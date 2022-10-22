var cardGuts = `<a href="https://mohessaid.com" class="card">
  <div class="card-thumbnail"></div>
  <div class="card-body">
    <h1 class="card-title">Yet Another Card</h1>
    <p class="card-text">This is a test for our new card. Really, it's nothing fancy. But we like it.</p>
  </div>`;

var cardTop = `<a href="https://mohessaid.com" class="card">
  <div class="card-thumbnail"></div>
  <div class="card-body">
    <h1 class="card-title">`;
var cardMid = `</h1>
    <p class="card-text">`;
var cardBot = `</p>
  </div>`;

function plate(dict){
  var key;
  /*for (pair in dict) {
    document.getElementById("container").innerHTML += cardGuts;
  alert("add");
  }  */
  for (var key in dict) {
    if (dict.hasOwnProperty(key)) {
        document.getElementById("container").innerHTML += cardTop + key;
       document.getElementById("container").innerHTML += cardMid + dict[key];
       document.getElementById("container").innerHTML += cardBot;
    }
}
}

plate({
                "level": 2,
                "events": 2,
                "streak": 2,
                "percent_category": 2,
                "XP": 2,
                "number_of_city_visited":2,
                "number_of_country_visited": 2,
                "number_of_events":2,
                "number_of_threads": 2,
            });