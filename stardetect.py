from math import sqrt
import itertools

f = open('starSet1.star' ,"r")
lines = f.readlines()
f.close()

class Star:
	def __init__(self, x, y ):
		super(Star, self).__init__()
		self.x = x
		self.y = y

class Constellation:
	def __init__(self, num,tri=None , stars=None, matchScore=None):
		self.n = num
		self.triangles = tri
		self.stars = stars
		self.matchScore = matchScore

stars = [ [int(l[:-1].split(',')[0]), int(l[:-1].split(',')[1])] for l in lines ]
constellationStars1 =  [stars[0]] + stars[2:5]
constellationStars2 =  [stars[1]] + stars[6:8] # all stars different from constellationStars1
constellationStars3 =  [stars[1]] + stars[2:5] # one star different from constellationStars1

def triangleMap(starset):
	triangleSides = [];
	trianglesSet = permute3(starset)
	for triangle in trianglesSet:
		triangleSides.append(convertToRatio(calculateSides(triangle)))
	return triangleSides


def permute3(starset):
	trianglesSet = [];
	n = len(starset);
	for i in xrange(0,n-2):
		for j in xrange(i+1,n-1):
			for k in xrange(j+1,n):
				trianglesSet.append([starset[i],starset[j],starset[k]]);
	return trianglesSet;

def permuteN(starset,N):
	
	permuteDB = []
	target = N
	size = len(starset)
	for i in itertools.product( [0,1], repeat=size):
		sum=0
		for j in i:
			sum+=j
		if sum==target:
			permuteCandidate = []
			counter = 0
			for j in i:
				if j==1:
					permuteCandidate.append(starset[counter])
				counter += 1
			permuteDB.append(permuteCandidate)

	return permuteDB

def calculateSides(triangle):
	sides = [];
	sides.append(dist2Points([triangle[0],triangle[1]]));
	sides.append(dist2Points([triangle[1],triangle[2]]));
	sides.append(dist2Points([triangle[2],triangle[0]]));
	return sides;

def dist2Points(points):
	return sqrt((points[0][0] - points[1][0])**2  + (points[0][1] - points[1][1])**2 );

def convertToRatio(vector):
	vector.sort();
	vectorRatio = [l/vector[0] for l in vector];
	return vectorRatio;


def constellationMatch( constellationA, constellationB):
	# to find if constellationA is similar to constellationB.
	# done by counting the number of triangles which are similar amongst set A and set B.
	# generate a similarity count.
	# note down if a significant count exists, add it to db.
	
	# tweak matchTolerance

	matchScore = 0.0

	trisetA = constellationA.triangles
	trisetB = constellationB.triangles
	triNum	= len(trisetA)

	for triA in trisetA:
		for triB in trisetB:
			if (matches(triA, triB)):
				matchScore += 1.0

	return matchScore


def matches(triA,triB):
	matchTolerance = 0.001
	rms = sqrt( (triA[1]-triB[1])**2 + (triA[2]-triB[2])**2 )/2
	if (rms < matchTolerance):
		print rms
		return True
	else:
		return False



""" defining the constellation based on previous data """
fourStarCons1 = Constellation(4, tri=triangleMap(constellationStars1), stars=constellationStars1);
fourStarCons2 = Constellation(4, tri=triangleMap(constellationStars2), stars=constellationStars2);
fourStarCons3 = Constellation(4, tri=triangleMap(constellationStars3), stars=constellationStars3);

print constellationMatch (fourStarCons3, fourStarCons2)
# starSpacePerms = permuteN()
# permute 4 constellation stars from universal starset
# use each of it to check if matches with the one to detect
# generate matchScore and sort with matchScore to generate final detection result.