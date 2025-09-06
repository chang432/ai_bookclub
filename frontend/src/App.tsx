import './App.css'
import Header from './components/Header'
import Book from "./components/Book"
import PostList from "./components/PostList"

function App() {

  return (
    <div className="flex flex-col items-center space-y-20 border p-10">
      <Header />
      <Book />
      <PostList />
    </div>
  )
}

export default App
