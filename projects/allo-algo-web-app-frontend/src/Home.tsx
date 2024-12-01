// src/components/Home.tsx
import { motion } from 'framer-motion'
import { ArrowDownIcon } from 'lucide-react'
import React from 'react'
import Features from './components/Features'
import Footer from './components/Footer'
import Header from './components/Header'
import Hero from './components/Hero'

interface HomeProps {}

const Home: React.FC<HomeProps> = () => {
  console.log('hii')
  return (
    <>
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white">
        <Header />
        <Hero />
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 0.5 }}
          className="flex justify-center my-12"
        >
          <ArrowDownIcon className="w-8 h-8 animate-bounce" />
        </motion.div>
        <Features />
        <Footer />
      </div>
    </>
  )
}
// const Home: React.FC<HomeProps> = () => {
// const [openWalletModal, setOpenWalletModal] = useState<boolean>(false)
// const [openDemoModal, setOpenDemoModal] = useState<boolean>(false)
// const [appCallsDemoModal, setAppCallsDemoModal] = useState<boolean>(false)
// const { activeAddress } = useWallet()

// const toggleWalletModal = () => {
//   setOpenWalletModal(!openWalletModal)
// }

// const toggleDemoModal = () => {
//   setOpenDemoModal(!openDemoModal)
// }

// const toggleAppCallsModal = () => {
//   setAppCallsDemoModal(!appCallsDemoModal)
// }

//   return (
//     <div className="hero min-h-screen bg-teal-400">
//       <div className="hero-content text-center rounded-lg p-6 max-w-md bg-white mx-auto">
//         <div className="max-w-md">
//           <h1 className="text-4xl">
//             Welcome to <div className="font-bold">AlgoKit 🙂</div>
//           </h1>
//           <p className="py-6">
//             This starter has been generated using official AlgoKit React template. Refer to the resource below for next steps.
//           </p>

//           <div className="grid">
//             <a
//               data-test-id="getting-started"
//               className="btn btn-primary m-2"
//               target="_blank"
//               href="https://github.com/algorandfoundation/algokit-cli"
//             >
//               Getting started
//             </a>

//             <div className="divider" />
//             <button data-test-id="connect-wallet" className="btn m-2" onClick={toggleWalletModal}>
//               Wallet Connection
//             </button>
//             <Button>HI</Button>
//             {activeAddress && (
//               <button data-test-id="transactions-demo" className="btn m-2" onClick={toggleDemoModal}>
//                 Transactions Demo
//               </button>
//             )}

//             {activeAddress && (
//               <button data-test-id="appcalls-demo" className="btn m-2" onClick={toggleAppCallsModal}>
//                 Contract Interactions Demo
//               </button>
//             )}
//           </div>

//           <ConnectWallet openModal={openWalletModal} closeModal={toggleWalletModal} />
//           <Transact openModal={openDemoModal} setModalState={setOpenDemoModal} />
//           <AppCalls openModal={appCallsDemoModal} setModalState={setAppCallsDemoModal} />
//         </div>
//       </div>
//     </div>
//   )
// }

export default Home
