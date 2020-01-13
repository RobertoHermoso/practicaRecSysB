from django.shortcuts import render, render_to_response
import pandas as pd
from .forms import *
from .models import Libro, Puntuacion

# Create your views here.
def populate_db(request):
    populate()


def sim_distance(prefs, person1, person2):
  # Get the list of shared_items
  si = {}
  for item in prefs[person1]: 
    if item in prefs[person2]: si[item] = 1
 
  # if they have no ratings in common, return 0
  if len(si) == 0: return 0
 
  # Add up the squares of all the differences
  sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2) 
                      for item in prefs[person1] if item in prefs[person2]])
 
  return 1 / (1 + sum_of_squares)

 
def sim_pearson(prefs, p1, p2):
  # Get the list of mutually rated items
  si = {}
  for item in prefs[p1]: 
    if item in prefs[p2]: si[item] = 1
 
  # if they are no ratings in common, return 0
  if len(si) == 0: return 0
 
  # Sum calculations
  n = len(si)
   
  # Sums of all the preferences
  sum1 = sum([prefs[p1][it] for it in si])
  sum2 = sum([prefs[p2][it] for it in si])
   
  # Sums of the squares
  sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
  sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])    
   
  # Sum of the products
  pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])
   
  # Calculate r (Pearson score)
  num = pSum - (sum1 * sum2 / n)
  den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
  if den == 0: return 0
 
  r = num / den
   
  return r

 
def topMatches(prefs, person, n=5, similarity=sim_pearson):
  scores = [(similarity(prefs, person, other), other) 
                  for other in prefs if other != person]
 
  scores.sort()
  scores.reverse()
  return scores[0:n]
 
 
def getRecommendations(prefs, person, similarity=sim_pearson):
  totals = {}
  simSums = {}
  for other in prefs:
    # don't compare me to myself
    if other == person: continue
    sim = similarity(prefs, person, other)
 
    # ignore scores of zero or lower
    if sim <= 0: continue
    for item in prefs[other]:
         
      # only score movies I haven't seen yet
      if item not in prefs[person] or prefs[person][item] == 0:
        # Similarity * Score
        totals.setdefault(item, 0)
        totals[item] += prefs[other][item] * sim
        # Sum of similarities
        simSums.setdefault(item, 0)
        simSums[item] += sim
 
  # Create the normalized list
  rankings = [(total / simSums[item], item) for item, total in totals.items()]
 
  # Return the sorted list
  rankings.sort()
  rankings.reverse()
  return rankings   

 
def transformPrefs(prefs):
  result = {}
  for person in prefs:
    for item in prefs[person]:
      result.setdefault(item, {})
       
      # Flip item and person
      result[item][person] = prefs[person][item]
  return result

 
def calculateSimilarItems(prefs, user, n=10):
  # Create a dictionary of items showing which other items they
  # are most similar to.
  scores = {}
  # Invert the preference matrix to be item-centric
#   itemPrefs=transformPrefs(prefs) #Not needed in this case
  for item in prefs:
    if item == user:
        scores = topMatches(prefs, item, n=n, similarity=sim_distance)
        break
  return scores

 
def recommended_books(request):
     
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form['usuario'].value()
            usuarios = Puntuacion.objects.order_by().values('idUsuario').distinct()
            dict = {}
             
            for u in usuarios:
                u = u["idUsuario"]
                p_dict = {}
                puntuaciones = Puntuacion.objects.all().filter(idUsuario=u)
                for p in puntuaciones:
                    id = p.bookId.bookId
                    b = Libro.objects.filter(bookId=id)[0]
                    p_dict[b.titulo] = p.puntuacion
                     
                dict[u] = p_dict
            print(dict)
            books = getRecommendations(dict, user)
            return render(request, 'recomendaciones.html', {'books': books, 'form':form})
 
    else:
        form = UsuarioForm()
 
    return render(request, 'recomendaciones.html', {'form': form})

 
def similar_users(request):
      
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form['usuario'].value()
            usuarios = Puntuacion.objects.order_by().values('idUsuario').distinct()
            dict = {}
              
            for u in usuarios:
                u = u["idUsuario"]
                print(u)
                p_dict = {}
                puntuaciones = Puntuacion.objects.all().filter(idUsuario=u)
                for p in puntuaciones:
                    id = p.bookId.bookId
                    b = Libro.objects.filter(bookId=id)[0]
                    print(b)
                    p_dict[b.titulo] = p.puntuacion
                     
                dict[u] = p_dict
            print(dict)
            books = calculateSimilarItems(dict, user)
            return render(request, 'similares.html', {'user' : user, 'books': books, 'form':form})
  
    else:
        form = UsuarioForm()
  
    return render(request, 'similares.html', {'form': form})



def best_libros(request):
    libros = Libro.objects.all()
    print(libros)
    res = sorted(libros, key=lambda libro: (libro.num_ratings_1 + libro.num_ratings_2 * 2 + libro.num_ratings_2 * 3 + libro.num_ratings_4 * 4 + libro.num_ratings_5 * 5) / (libro.num_ratings_1 + libro.num_ratings_2 + libro.num_ratings_3 + libro.num_ratings_4 + libro.num_ratings_5), reverse=True)
    del res[3:]
    resFinal = []
    for libro in res:
        resFinal.append(libro.titulo + ' -->  ' + str((libro.num_ratings_1 + libro.num_ratings_2 * 2 + libro.num_ratings_2 * 3 + libro.num_ratings_4 * 4 + libro.num_ratings_5 * 5) / (libro.num_ratings_1 + libro.num_ratings_2 + libro.num_ratings_3 + libro.num_ratings_4 + libro.num_ratings_5)))

    return render_to_response('best_libros.html', {'res': resFinal})


def home(request):

    return render_to_response('home.html')



#Populate
def populate():

    books = pd.read_csv('data/bookfeatures.csv', sep=';')
    ratings = pd.read_csv('data/ratings.csv', sep=';')
    for i, book in books.iterrows():
        rating1 = book['rating1']
        if rating1 == 'NaN':
            rating1 = 0
        rating2 = book['rating2']
        if rating2 == 'NaN':
            rating2 = 0
        rating3 = book['rating3']
        if rating3 == 'NaN':
            rating3 = 0
        rating4 = book['rating4']
        if rating4 == 'NaN':
            rating4 = 0
        rating5 = book['rating5']
        if rating5 == 'NaN':
            rating5 = 0
        print(book)
           
        b = Libro.objects.get_or_create(bookId=book['bookid'], titulo=book['name'], autor=book['author'],genero=book['genre'], idioma=book['lang'], num_ratings_1=rating1,num_ratings_2=rating2,num_ratings_3=rating3,num_ratings_4=rating4,num_ratings_5=rating5)[0]
        b.save()
           
      
    for i, rating in ratings.iterrows():
        book = Libro.objects.get(bookId=rating['bookid'])
        book_rating = Puntuacion(idUsuario=rating['user'], bookId=book, puntuacion=rating['ratings'])
        book_rating.save()


    
def libro_genero_list(request):
    books = {}
    libros = Libro.objects.all()
    if request.method == 'GET':
        form = GeneroForm(request.GET, request.FILES)
        if form.is_valid():
            genero = form['genero'].value()
            try:
                books = Libro.objects.filter(genero=genero)
                print(books)
            except:
                pass
    else:
        form = GeneroForm()


    return render_to_response('libro_genero_list.html', {'form': form, 'books': books})