#!/usr/bin/env python3
import statistics #for std
import numpy as np #for Pearson r coeffecient

'''
 Function: store_movie_names() takes the data from file
  movie-names.txt and stores each movie into a list.
'''
def store_movie_names():
    #Need Special encoding for the file we are using
    with open('movie-names.txt','r',encoding="ISO-8859-1") as fd:
     file=fd.read()
    
    movieNames=[x for x in file.splitlines()]
    return movieNames

'''
 Function: store_movie_matrix() takes the data from file
  movie-matrix.txt and stores each row as a list, creating
  a list of lists. Using enumerate we can create inner touples 
  of (reviewer#, rating)_
'''

def store_movie_matrix():
    #Need Special encoding for the file we are using
    with open('movie-matrix.txt','r',encoding="ISO-8859-1") as fd:
     file=fd.read()
    
    reviews=[]
    
    for line in file.splitlines():
        x=line.split(';')
        temp=[]
       
        for e in enumerate(x,1):
            temp.append(e)
          
        reviews.append(temp)
    return reviews

'''
Function compute_r(m1,m2,movieMatrix) takes in target and comparison movies
and the movie matrix as a paramater. It computes the r value of both movies
to identify if it makes for a good recommended movie.
'''
def compute_r(m1,m2,movieMatrix):

 
    #1.Get Each person that reviewed each movie
    reviewers_movie1=[int(x[0]) for x in movieMatrix[m1-1] if x[1].isdigit()]
    reviewers_movie2=[int(x[0]) for x in movieMatrix[m2-1] if x[1].isdigit()]


    #2.See the shared reviewers between both movies +
    shared_reviewers=[x for x in reviewers_movie1 if x in reviewers_movie2]


    #3.For each shared reviewer, see the review for each movie 
    shared_reviews_form__reviewers_movie1= [int(x[1]) for x in movieMatrix[m1-1] if x[0] in shared_reviewers]
    shared_reviews_form__reviewers_movie2=[int(x[1]) for x in movieMatrix[m2-1] if x[0] in shared_reviewers]
    
    #4. Load the reviews of each into numpy arrays that will allow to use
    #   numpy functions such as to compute r.
    x=np.array(shared_reviews_form__reviewers_movie1)
    y=np.array(shared_reviews_form__reviewers_movie2)

    #5. Compute Correleation coeffecient r for both movies
    r=np.corrcoef(x,y)
    return r[0][1]

'''
Function CompareMovies--- compare if movies are eligable to compute r.
 If less than 10 then it is not.
'''
def CompareMovies(m1,m2,movieMatrix):

    #compare to see if more than 10 people rated that movie
    #Each person that reviewed each movie
    reviewers_movie1=[x[0] for x in movieMatrix[m1-1] if x[1].isdigit()]
    reviewers_movie2=[x[0] for x in movieMatrix[m2-1] if x[1].isdigit()]

    #common people for both movies
    common_reviewers=[x for x in reviewers_movie1 if x in reviewers_movie2]

    #if less than 10 reviewers then dont use
    if len(common_reviewers)<11:
        pass
    else:
        #Compute r
        r=compute_r(m1,m2,movieMatrix)
        return r,m2,len(common_reviewers)

def main():

    #Creating the variables containg the stored data
    movieNames=store_movie_names()
    movieMatrix=store_movie_matrix()

    #Begin output
    print("*** No. of rows (movies) in matrix =",len(movieMatrix))
    print("*** No. of columns (reviewers) =",len([x for x in movieMatrix[0]]) ) 
    
    movie1=input("Enter Movie Number:")
    goal=False
    
    #Make sure the desired input is made 
    while goal==False:

        if movie1.isdigit()==False:
            print("\nMovie:",movie1," Movie must be numeric")
            movie1=input()


        if int(movie1)<=0 or int(movie1)>len(movieNames):
            print("\nMovie:",movie1,"Movie number must be between 1 and 1682")
            movie1=input()
        else:
            goal=True

    #Variables to use
    movie1=int(movie1)      #Once desired input made, convert to int
    print("\nMovie:",movieNames[movie1-1])
    movie2=1                #movie2 used for movie of comparison
    total_movies_compared=0 #grabs total number of comparisons made to movie
    movies_compared_to=[]   #holds index of all movies compared

    #While there are remaining movies to compare to
    while movie2<=len(movieNames):

        #store comparison data in results, add to movies compared too 
        result=CompareMovies(movie1,movie2,movieMatrix)
        movies_compared_to.append(result)
        #Movie to next movie index
        movie2+=1

    #Remove all the movies that didnt have enough reviews for comparison
    movies_compared_to=[x for x in movies_compared_to if x !=None]

    #sort movies based off r-score. Greatest to Least.
    movies_compared_to.sort(reverse=True)

    #Print Proper output
    print(" #\tR\tNo.\tReviews\t\t\tName")

    #Only print top 20 movies 
    movies_compared_to=movies_compared_to[0:20]

    #If there werent at least 20 movies to compare to then not enough data
    if len(movies_compared_to)<20:
        print("Insuffecient movies to compare")

    else:
        count=1 # movie # flag 
        for x in movies_compared_to:

            print("{0:2}".format(count),"{0:3.6f}".format(x[0]),"{0:7}".format(x[1]),"\t({0} reviews)".format(x[2]),'\t',movieNames[x[1]-1].split('|')[1])
            count+=1

#Call main()       
if __name__ == "__main__":
    main()
    
 

    
 

