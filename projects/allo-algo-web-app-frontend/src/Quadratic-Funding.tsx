'use client'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { QuadraticFundingClient } from '@/contracts/QuadraticFunding'
import * as algokit from '@algorandfoundation/algokit-utils'
import { TransactionSignerAccount } from '@algorandfoundation/algokit-utils/types/account'
import { useWallet } from '@txnlab/use-wallet'
import algosdk from 'algosdk'
import { motion } from 'framer-motion'
import { useEffect, useState } from 'react'
import { toast, ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import one from '../public/1.png'
import two from '../public/2.jpeg'
import three from '../public/3.png'
import { getAlgodConfigFromViteEnvironment } from './utils/network/getAlgoClientConfigs'
interface Project {
  id: number
  title: string
  description: string
  image: string
  directDonations: number
  uniqueDonors: number
}

const projects: Project[] = [
  {
    id: 0,
    title: 'Green Earth Initiative',
    description: 'Promoting sustainable practices and environmental conservation.',
    image: two,
    directDonations: 1.3,
    uniqueDonors: 2,
  },
  {
    id: 1,
    title: 'Tech Education for All',
    description: 'Providing access to technology education in underserved communities.',
    image: one,
    directDonations: 1.5,
    uniqueDonors: 1,
  },
  {
    id: 2,
    title: 'Health First',
    description: 'Improving healthcare access and awareness in rural areas.',
    image: three,
    directDonations: 1.5,
    uniqueDonors: 1,
  },
]

const QF_ADDRESS = '7WHQK5Z435OQPH4LTAUMYFPW7M53WLGUSHQLYA5TUPDSHQF4UT4C7KIEKE'
const APP_ID = 730129661
export default function QuadraticFunding() {
  const [totalMatchingPool, setTotalMatchingPool] = useState<number>(0)
  const { signer, activeAddress } = useWallet()
  const [donations, setDonations] = useState<{ [key: number]: number }>({})
  const [matchingEstimates, setMatchingEstimates] = useState<{ [key: number]: number }>({})

  const algodConfig = getAlgodConfigFromViteEnvironment()
  const algodClient = algokit.getAlgoClient({
    server: algodConfig.server,
    port: algodConfig.port,
    token: algodConfig.token,
  })

  useEffect(() => {
    const initialMatchingPool = projects.reduce((sum, project) => sum + project.directDonations, 0)
    setTotalMatchingPool(initialMatchingPool)
    calculateMatching(initialMatchingPool)
  }, [])

  const handleDonate = async (projectId: number, amount: number) => {
    if (amount <= 0) {
      toast.error('Please enter a valid donation amount')
      return
    }
    if (!activeAddress) {
      toast.error('Please connect your wallet')
      return
    }
    setDonations((prev) => ({
      ...prev,
      [projectId]: (prev[projectId] || 0) + amount,
    }))
    const quadraticClient = new QuadraticFundingClient(
      {
        resolveBy: 'id',
        id: APP_ID,
        sender: { signer, addr: activeAddress } as TransactionSignerAccount,
      },
      algodClient,
    )
    const suggestedParams = await algodClient.getTransactionParams().do()

    const transaction = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
      from: activeAddress,
      to: QF_ADDRESS,
      amount: amount * 1e6,
      suggestedParams,
    })

    // algokit.getBoxReference({

    // })
    const a = await quadraticClient.appClient.getBoxNames()
    const finalBox = a.map((box) => {
      return {
        appIndex: APP_ID,
        name: box.nameRaw,
      } as algosdk.BoxReference
    })
    await quadraticClient
      .compose()
      .addTransaction(transaction)
      .donate(
        {
          proposalId: projectId,
          amountMicroAlgo: amount * 1e6,
        },
        {
          accounts: [activeAddress],
          boxes: finalBox,
        },
      )
      .execute()

    // const encodedTransaction = algosdk.encodeUnsignedTransaction(transaction)

    // const signedTransactions = await signTransactions([encodedTransaction])
    const newTotalMatchingPool = totalMatchingPool + amount
    setTotalMatchingPool(newTotalMatchingPool)
    calculateMatching(newTotalMatchingPool)
    toast.success(`Donated ${amount} 
        to project ${projectId}`)
  }

  const calculateMatching = (matchingPool: number) => {
    let totalSqrtSum = 0
    const sqrtSums: { [key: number]: number } = {}

    projects.forEach((project) => {
      const totalDonations = project.directDonations + (donations[project.id] || 0)
      const sqrtSum = Math.sqrt(totalDonations) * Math.sqrt(project.uniqueDonors)
      sqrtSums[project.id] = sqrtSum
      totalSqrtSum += sqrtSum
    })

    const newMatchingEstimates: { [key: number]: number } = {}
    projects.forEach((project) => {
      const matchingAmount = (sqrtSums[project.id] / totalSqrtSum) * matchingPool
      newMatchingEstimates[project.id] = matchingAmount
    })

    setMatchingEstimates(newMatchingEstimates)
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white p-8">
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-4xl mx-auto"
      >
        <h1 className="text-4xl font-bold mb-8 text-center">Quadratic Funding Projects</h1>
        <div className="mb-8">
          <p className="text-xl mb-2">Total Matching Pool: Algo {totalMatchingPool.toFixed(2)}</p>
          <p className="text-sm text-gray-400 mb-4">The matching pool increases with each donation.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {projects.map((project) => (
            <motion.div key={project.id} whileHover={{ scale: 1.05 }} className="bg-gray-800 rounded-lg shadow-xl p-6">
              <img src={project.image} alt={project.title} width={200} height={200} className="w-full h-48 object-cover rounded-lg mb-4" />
              <h2 className="text-2xl font-bold mb-2">{project.title}</h2>
              <p className="text-gray-300 mb-4">{project.description}</p>
              <p className="mb-2">Direct Donations: Algo {project.directDonations + (donations[project.id] || 0)}</p>
              <p className="mb-2">Unique Donors: {project.uniqueDonors}</p>
              <p className="mb-4 text-green-400 font-bold">
                Estimated Matching: Algo {matchingEstimates[project.id]?.toFixed(2) || '0.00'}
              </p>
              <Input
                type="number"
                placeholder="Donation Amount"
                className="w-full bg-gray-700 text-white mb-2"
                onChange={(e) => setDonations((prev) => ({ ...prev, [project.id]: Number(e.target.value) }))}
              />
              <Button onClick={() => handleDonate(project.id, donations[project.id] || 0)} className="w-full bg-blue-500 hover:bg-blue-600">
                Donate
              </Button>
            </motion.div>
          ))}
        </div>
      </motion.div>
      <ToastContainer position="bottom-right" theme="dark" />
    </div>
  )
}
