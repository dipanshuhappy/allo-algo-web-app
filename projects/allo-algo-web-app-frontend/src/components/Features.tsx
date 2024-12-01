import { motion } from 'framer-motion'
import { BookOpenIcon, CoinsIcon, LightbulbIcon as LightBulbIcon } from 'lucide-react'

const features = [
  {
    title: 'Registry',
    description: 'Set up your project and define parameters for fund allocation.',
    icon: BookOpenIcon,
  },
  {
    title: 'Strategy',
    description: 'Choose from various allocation strategies, including quadratic funding.',
    icon: LightBulbIcon,
  },
  {
    title: 'Allocate',
    description: 'Distribute funds efficiently based on the chosen strategy.',
    icon: CoinsIcon,
  },
]

export default function Features() {
  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8">
      <h2 className="text-3xl font-bold text-center mb-12">How Allo Algo Works</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
        {features.map((feature, index) => (
          <motion.div
            key={feature.title}
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.2 }}
            className="bg-gray-800 p-6 rounded-lg shadow-lg"
          >
            <feature.icon className="w-12 h-12 mb-4 text-green-500" />
            <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
            <p className="text-gray-300">{feature.description}</p>
          </motion.div>
        ))}
      </div>
    </section>
  )
}
