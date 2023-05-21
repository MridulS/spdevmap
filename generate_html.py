import tomllib
from pathlib import Path

with open("data.toml", "rb") as f:
    data = tomllib.load(f)


def marker_generator(data):
    for user in data:
        yield f"""L.marker([{user['lat']}, {user['long']}]).addTo(map).bindPopup('<a href="{user['url']}" target="_blank">{user['display_name']}<a>');"""


html_marker = "\n".join(marker_generator(d for d in data.values()))

raw_html = f"""<html>
      <head>
           <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css"
       integrity="sha256-kLaT2GOSpHechhsozzB+flnD+zUyjE2LlfWPgU04xyI="
       crossorigin=""/>
            <script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js"
       integrity="sha256-WBkoXOwTeyKclOHuWtc+i2uENFpDZ9YPdf5Hf+D7ewM="
       crossorigin=""></script>
              <style>
                  body {{ margin:0; padding:0; }}
                  #map {{ position: absolute; top:80; bottom:30; right:30; left:30; }}
              </style>
      </head>
      <body>
        <center> <h1>Where are the Scientific Python folks?</h1> </center>
          <div id="map"></div>
            <script>
              var map = L.map('map').setView([0, 0], 2);
              L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }}).addTo(map);
             {html_marker}
          </script>
      </body>
  </html>"""


file = Path("publish/index.html")
file.parent.mkdir(parents=True, exist_ok=True)
file.write_text(raw_html)
