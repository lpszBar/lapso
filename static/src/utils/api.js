export function fetchPhotos () {
  const endpoint = window.encodeURI(
  	`http://0.0.0.0:5000/api/photos`
  	)

  return fetch(endpoint)
    .then((res) => res.json())
    .then((data) => {
      if (!data.photos) {
        throw new Error(data.message)
      }
    	console.log("data es -" + JSON.stringify(data.photos) + "-")

      return data.photos
    })
    .catch(err => console.error(err))
}