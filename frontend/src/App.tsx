import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Header from './components/Header'
import Book from "./components/Book"
import PostList from "./components/PostList"

function App() {

  return (
    <div className="flex flex-col items-center space-y-20 border p-10">
      <Header />
      <Book date="08/24/25" title="Project Hail Mary" author="Andy Weir" />
      <PostList />
    </div>
  )
}

export default App
