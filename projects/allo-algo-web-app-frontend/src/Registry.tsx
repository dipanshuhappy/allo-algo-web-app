'use client'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import * as algokit from '@algorandfoundation/algokit-utils'
import { useWallet } from '@txnlab/use-wallet'
import algosdk from 'algosdk'
import { motion } from 'framer-motion'
import { enqueueSnackbar } from 'notistack'
import { useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { toast, ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import { delay } from './lib/utils'
import { getAlgodConfigFromViteEnvironment } from './utils/network/getAlgoClientConfigs'
function stringToUint8Array(input: string): Uint8Array {
  const encoder = new TextEncoder()
  return encoder.encode(input)
}

export default function Registry() {
  const [projectName, setProjectName] = useState('')
  const [description, setDescription] = useState('')
  const [image, setImage] = useState<File | null>(null)
  // const { signer, activeAddress } = useWallet()

  const onDrop = (acceptedFiles: File[]) => {
    setImage(acceptedFiles[0])
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/*': [] },
    multiple: false,
  })

  const { signer, activeAddress, signTransactions, sendTransactions } = useWallet()
  const algodConfig = getAlgodConfigFromViteEnvironment()
  const algodClient = algokit.getAlgoClient({
    server: algodConfig.server,
    port: algodConfig.port,
    token: algodConfig.token,
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!projectName || !description || !image) {
      toast.error('Please fill in all fields and upload an image.')
      return
    }
    enqueueSnackbar('Loading', { variant: 'default' })
    // Here you would typically send the data to your backend
    // toast.success('Project registered successfully!')
    // Reset form
    console.log({ activeAddress })
    // const registry = new RegistryClient(
    //   {
    //     resolveBy: 'id',
    //     id: 729700368,
    //     sender: { signer, addr: activeAddress } as TransactionSignerAccount,
    //   },
    //   algodClient,
    // )

    await delay(4000)
    if (!signer || !activeAddress) {
      enqueueSnackbar('Please connect wallet first', { variant: 'warning' })
      return
    }

    const suggestedParams = await algodClient.getTransactionParams().do()

    const transaction = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
      from: activeAddress,
      to: '7E235EWWTMM2GKBIHTMN5OZBWUQWHKR7ZZTOND3LN3AQ3IZIO2CJ3ITVOA',
      amount: 1e5,
      suggestedParams,
    })

    const encodedTransaction = algosdk.encodeUnsignedTransaction(transaction)

    const signedTransactions = await signTransactions([encodedTransaction])

    const waitRoundsToConfirm = 4

    try {
      enqueueSnackbar('Sending transaction...', { variant: 'info' })
      const { id } = await sendTransactions(signedTransactions, waitRoundsToConfirm)
    } catch (e) {
      enqueueSnackbar('Failed to send transaction', { variant: 'error' })
    }
    // enqueueSnackbar(`Response from the contract: ${response?.return}`, { variant: 'success' })

    setProjectName('')
    setDescription('')
    setImage(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white p-8">
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-2xl mx-auto bg-gray-800 rounded-lg shadow-xl p-8"
      >
        <h1 className="text-4xl font-bold mb-8 text-center">Register Your Project</h1>
        <form onSubmit={handleSubmit} className="space-y-6">
          <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
            <Input
              type="text"
              placeholder="Project Name"
              value={projectName}
              onChange={(e) => setProjectName(e.target.value)}
              className="w-full bg-gray-700 text-white"
            />
          </motion.div>
          <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
            <Textarea
              placeholder="Project Description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full bg-gray-700 text-white"
              rows={4}
            />
          </motion.div>
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer ${
              isDragActive ? 'border-green-500' : 'border-gray-600'
            }`}
          >
            <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
              <input {...getInputProps()} />
              {image ? (
                <p>Image uploaded: {image.name}</p>
              ) : isDragActive ? (
                <p>Drop the image here ...</p>
              ) : (
                <p>Drag 'n' drop an image here, or click to select one</p>
              )}
            </motion.div>
          </div>
          <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
            <Button type="submit" className="w-full bg-green-500 hover:bg-green-600">
              Register Project
            </Button>
          </motion.div>
        </form>
      </motion.div>
      <ToastContainer position="bottom-right" theme="dark" />
    </div>
  )
}
