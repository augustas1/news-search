import { QueryClientProvider, QueryClient } from '@tanstack/react-query'
import { NewsSearch } from "./news/NewsSearch"

function App() {
  return (
    <QueryClientProvider client={new QueryClient()}>
      <div className='max-w-4xl my-8 mx-auto px-8'>
        <NewsSearch />
      </div>
    </QueryClientProvider>
  )
}

export default App
