import React from 'react';
import logo from './logo.svg';
import './App.css';


function Book(props) {

  return (
    <ul>
     {props.photos.map( (photo) => 
       <li key={photo.id}>
        <img src={photo.url} />
       </li>
      )}
    </ul>
  )
}

function App() {
  let photos = [
    {'id': 1, 
      'url': 'http://checklist.onlineflora.cn/sites/default/files/styles/slideshow_large/public/20130401.jpg?itok=KbGQz4e7'},
    {'id': 2, 
      'url': "http://checklist.onlineflora.cn/sites/default/files/styles/slideshow_large/public/2013%20%283%29.JPG?itok=oCRIMemI"},
  ]
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
           edit <code>src/App.js</code> and save to reload.
        </p>
      </header>
      <Book className="App-book" photos={photos}/>
    </div>
  );
}

export default App;
