import requests
import bs4


url = "https://cinestar.pk/Browsing/Movies/NowShowing"
response = requests.get(url)
print(response.status_code)

# soup = bs4.BeautifulSoup(response.text, 'html.parser')
# print(soup.prettify())

# movies = []

# for movie_div in soup.find_all("div", class_="list-item movie"):

#     image_outer = movie_div.find("div", class_="image-outer")
#     img_tag = image_outer.find("img") if image_outer else None
#     image_url = img_tag["src"] if img_tag and img_tag.has_attr("src") else None

#     if image_url and image_url.startswith("//"):
#         image_url = "https:" + image_url

#     name_class = movie_div.find("h3", class_="item-title")
#     name = name_class.get_text(strip=True) if name_class else "No title"

#     desc_class = movie_div.find("p", class_="blurb subtext")
#     description = desc_class.get_text(strip=True) if desc_class else "No description"

#     movies.append({
#         "name": name,
#         "description": description,
#         "image": image_url
#     })

# print("Now Showing")
# for m in movies[:5]:
#     print(f"Movie: {m['name']}")
#     print(f"Description: {m['description']}")
#     print(f"Image: {m['image']}")

#     print("-" * 40)


data = response.json()
movies = response.json()["movies"]
print(movies)

'''
div class="now-showing" id="movies">
     <h2>
      <em>
       Now Showing
      </em>
     </h2>
     <div class="ad-content">
      <section class="loading main-ad generic-image-carousel">
      </section>
      <section class="loading lower-ad generic-image-carousel">
      </section>
     </div>
     <article id="movies-list">
      <div class="list-item movie">
       <div class="image-outer">
        <div style="background-image: url('//cinestar.pk/CDN/media/entity/get/FilmPosterGraphic/h-HO00001064?width=121&amp;height=180&amp;referenceScheme=HeadOffice&amp;allowPlaceHolder=true')">
         <img src="//cinestar.pk/CDN/media/entity/get/FilmPosterGraphic/h-HO00001064?width=121&amp;height=180&amp;referenceScheme=HeadOffice&amp;allowPlaceHolder=true"/>
        </div>
        <a class="play" data-film-ho-code="THEHOU002" data-movie-id="h-HO00001064" href="https://www.youtube.com/watch?v=lGY1m0Bm4do">
         <div class="overlay">
         </div>
         <span>
          Play Trailer
         </span>
        </a>
       </div>
       <div class="item-details">
        <div class="item-details-inner">
        <div class="title-wrapper">
          <div class="censor-rating">
           <img class="icon" src="//cinestar.pk/CDN/media/entity/get/RatingIconGraphic/G?referenceScheme=Global&amp;allowPlaceHolder=true" title=""/>
          </div>
          <a href="//cinestar.pk/Browsing/Movies/Details/h-HO00001064">
           <h3 class="item-title">
            THE HOUSEMAID
           </h3>
          </a>
         </div>
         <p class="blurb subtext">
          A struggling young woman is relieved by the chance for a fresh start as a maid for a wealthy couple. Soon, she discovers that the family's secrets are far more dangerous than her own.
         </p>
        </div>
       </div>
       <div class="movie-actions">
        <div class="main-action">
         <span class="showtimes-book image-wrapper">
         </span>
         <a href="//cinestar.pk/Browsing/Movies/Details/h-HO00001064">
          View Show Times
         </a>
         <span class="right-arrow image-wrapper">
         </span>
        </div>
       </div>
      </div>
      <div class="list-item movie">
       <div class="image-outer">
        <div style="background-image: url('//cinestar.pk/CDN/media/entity/get/FilmPosterGraphic/h-HO00001058?width=121&amp;height=180&amp;referenceScheme=HeadOffice&amp;allowPlaceHolder=true')">
         <img src="//cinestar.pk/CDN/media/entity/get/FilmPosterGraphic/h-HO00001058?width=121&amp;height=180&amp;referenceScheme=HeadOffice&amp;allowPlaceHolder=true"/>
        </div>
        <a class="play" data-film-ho-code="ANACN002" data-movie-id="h-HO00001058" href="https://www.youtube.com/watch?v=az8M5Mai0X4">
         <div class="overlay">
         </div>
         <span>
          Play Trailer
         </span>
        </a>
       </div>
       <div class="item-details">
        <div class="item-details-inner">
         <div class="title-wrapper">
          <div class="censor-rating">
           <img class="icon" src="//cinestar.pk/CDN/media/entity/get/RatingIconGraphic/G?referenceScheme=Global&amp;allowPlaceHolder=true" title=""/>
          </div>
          <a href="//cinestar.pk/Browsing/Movies/Details/h-HO00001058">
           <h3 class="item-title">
            ANACONDA
           </h3>
          </a>
         </div>
         <p class="blurb subtext">
          A group of friends are going through a mid-life crisis. They decide to remake a favorite movie from their youth but encounter unexpected events when they enter the jungle.
         </p>
        </div>
       </div>
       <div class="movie-actions">
        <div class="main-action">
         <span class="showtimes-book image-wrapper">
         </span>
         <a href="//cinestar.pk/Browsing/Movies/Details/h-HO00001058">
          View Show Times
         </a>
         <span class="right-arrow image-wrapper">
         </span>
        </div>
       </div>
      </div>
      <div class="list-item movie">
       <div class="image-outer">
        <div style="background-image: url('//cinestar.pk/CDN/media/entity/get/FilmPosterGraphic/h-HO00000942?width=121&amp;height=180&amp;referenceScheme=HeadOffice&amp;allowPlaceHolder=true')">
         <img src="//cinestar.pk/CDN/media/entity/get/FilmPosterGraphic/h-HO00000942?width=121&amp;height=180&amp;referenceScheme=HeadOffice&amp;allowPlaceHolder=true"/>
        </div>
        <a class="play" data-film-ho-code="AVATFA002" data-movie-id="h-HO00000942" href="https://www.youtube.com/watch?v=7Nz0wG7vBhc">
         <div class="overlay">
         </div>
         <span>
          Play Trailer
         </span>
        </a>
       </div>
       <div class="item-details">
        <div class="item-details-inner">
         <div class="title-wrapper">
          <div class="censor-rating">
           <img class="icon" src="//cinestar.pk/CDN/media/entity/get/RatingIconGraphic/G?referenceScheme=Global&amp;allowPlaceHolder=true" title=""/>
          </div>
          <a href="//cinestar.pk/Browsing/Movies/Details/h-HO00000942">
           <h3 class="item-title">
            AVATAR: FIRE AND ASH
           </h3>
          </a>
         </div>
         <p class="blurb subtext">
          Jake and Neytiri's family grapples with grief after Neteyam's death, encountering a new, aggressive Na'vi tribe, the Ash People, who are led by the fiery Varang, as the conflict on Pandora escalates and a new moral focus emerges.
         </p>
        </div>
       </div>
       <div class="movie-actions">
        <div class="main-action">
         <span class="showtimes-book image-wrapper">
         </span>
         <a href="//cinestar.pk/Browsing/Movies/Details/h-HO00000942">
          View Show Times
         </a>
         <span class="right-arrow image-wrapper">
         </span>
        </div>
       </div>
      </div>
'''