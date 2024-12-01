import { motion } from 'framer-motion'

export default function Hero() {
  return (
    <motion.section
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1 }}
      className="text-center py-20 px-4 sm:px-6 lg:px-8"
    >
      <h1 className="text-5xl font-extrabold mb-6">Revolutionizing Capital Allocation on Algorand</h1>
      <p className="text-xl mb-8 max-w-3xl mx-auto">
        Allo Algo transforms how resources are distributed in the Algorand ecosystem. By leveraging smart contracts and innovative
        strategies, we're addressing coordination challenges and introducing new on-chain allocation methods.
      </p>
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className="bg-green-500 text-white px-8 py-3 rounded-full text-lg font-semibold hover:bg-green-600 transition-colors"
      >
        Get Started
      </motion.button>
    </motion.section>
  )
}
