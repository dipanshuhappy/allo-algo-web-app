import { useWallet } from '@txnlab/use-wallet'
import { motion } from 'framer-motion'
import { useState } from 'react'
import ConnectWallet from './ConnectWallet'
import { Button } from './ui/button'

export default function Header() {
  const [openWalletModal, setOpenWalletModal] = useState<boolean>(false)

  const { activeAddress } = useWallet()

  const toggleWalletModal = () => {
    setOpenWalletModal(!openWalletModal)
  }

  //   const toggleDemoModal = () => {
  //     setOpenDemoModal(!openDemoModal)
  //   }

  //   const toggleAppCallsModal = () => {
  //     setAppCallsDemoModal(!appCallsDemoModal)
  //   }

  return (
    <motion.header
      initial={{ opacity: 0, y: -50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="py-6 px-4 sm:px-6 lg:px-8"
    >
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Allo Algo</h1>
        <nav>
          <ul className="flex space-x-4">
            <li>
              <a href="#" className="hover:text-green-400 transition-colors">
                Registry
              </a>
            </li>
            <li>
              <Button variant="link" data-test-id="connect-wallet" className="text-white" onClick={toggleWalletModal}>
                Wallet Connection
              </Button>
            </li>
            <li>
              <a href="#" className="hover:text-green-400 transition-colors">
                Contact
              </a>
            </li>
          </ul>
        </nav>
      </div>
      <ConnectWallet openModal={openWalletModal} closeModal={toggleWalletModal} />
    </motion.header>
  )
}
