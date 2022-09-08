import logo from './logo.svg';
import './App.css';
import {useState} from 'react'
import axios from 'axios'
function App() {
  const [question , setQuestion] = useState('')
  const [answer , setAnswer] = useState('')
  const handleChange = (e) => {
    const question = e.target.value
    setQuestion(question) 
  }
  const handleClick = async () => {
    const data = {
      'question' : question
    }
    await axios.post('http://localhost:8000/predict/' , data)
    .then( res =>  setAnswer(res.data))

    var parent = document.getElementById('chatbox')
    var div = document.createElement("div");


    var userParentSpan = document.createElement('span') 
    userParentSpan.classList.add('chatChunk')
    var userChildSpan = document.createElement('span') 
    var userChildText = document.createTextNode('user') 
    var userParentText = document.createTextNode(question) 
    userChildSpan.append(userChildText ) 
    userParentSpan.append(userChildSpan)
    userParentSpan.append(userParentText) 

    var botParentSpan = document.createElement('span') 
    botParentSpan.classList.add('chatChunk')
    var botChildSpan = document.createElement('span') 
    var botChildText = document.createTextNode('bot') 
    var botParentText = document.createTextNode(answer) 
    console.log(botParentText)
    botChildSpan.append(botChildText ) 
    botParentSpan.append(botChildSpan)
    botParentSpan.append(botParentText) 


    div.append(userParentSpan) 
    div.append(botParentSpan)

    var border = document.createElement('hr') 

    parent.append(div)
    parent.append(border)
    

  }


  return (
    <div className="App">
      <header className="App-header">
        <h3>reddit chatbot</h3> 
        <div id='chatbox' >
           
        </div>
        <input value={question} onChange= {handleChange} placeholder ='question' /> 
        <button onClick={handleClick} >send</button>
      </header>
    </div>
  );
}

export default App;
