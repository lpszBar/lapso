import React from 'react';
import './App.css';
import {fetchPhotos} from './utils/api';

class Book extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      'photos': props.photos,
    }
  }

  componentDidMount () {
    fetchPhotos().then( (photos) => this.setState({photos: photos}) )
    console.log("montando")
  }

  render () {
    return (
      <ul>
       {this.state.photos.map( (photo) => 
         <li key={photo.id}>
          <img src={photo.object} alt="" width="400"/>
         </li>
        )}
      </ul>
    )
  }
}

// add propTypes to book


function App() {
  let photos = {
    'items':
    [
      {'id': 1, 
        'url': 'http://checklist.onlineflora.cn/sites/default/files/styles/slideshow_large/public/20130401.jpg?itok=KbGQz4e7'},
      {'id': 2, 
        'url': "http://checklist.onlineflora.cn/sites/default/files/styles/slideshow_large/public/2013%20%283%29.JPG?itok=oCRIMemI"},
    ]
  }
  return (
    <div className="App">
      <Book className="App-book" photos={photos.items}/>
    </div>
  );
}

export default App;
