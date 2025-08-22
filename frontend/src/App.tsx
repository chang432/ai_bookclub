import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Header from './components/Header'
import Book from "./components/Book"

function App() {

  return (
    <div className="flex flex-col">
      <Header />
      <Book title="Project Hail Mary" author="Andy Weir" />
    </div>
  )
}

export default App
