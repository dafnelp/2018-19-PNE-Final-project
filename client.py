import http.client
import json

# API information
PORT = 8000
SERVER = 'localhost'


def response(request):

    # Connect to the server
    conn = http.client.HTTPConnection(SERVER, PORT)

    # Send the request.
    conn.request("GET", request + "&json=1")

    # Wait for the server's response
    r1 = conn.getresponse()

    # Print the status
    print()
    print("Response received: ", end='')
    print(r1.status, r1.reason)

    # Read the response's body and close the connection
    data = r1.read().decode("utf-8")
    conn.close()

    # Generate the object from the json file
    response = json.loads(data)

    print(response)

    return

# In that part we are going to test some request

# Return the list of all the species
response("/listSpecies?")

# Return the list of only 12 species
response("/listSpecies?limit=12")

# Return the list of the chromosomes of one species
response("/karyotype?specie=mouse")

# Return the length of a chromosome, selecting the specie and the chromosome
response("/chromosomeLength?specie=dog&chromo=5")

# Return the sequence of a introduced gene
response("/geneSeq?gene=frat1")

# Return the information of a introduced gene
response("/geneInfo?gene=WASH7P")

# Return some calculations (length and percentage of the bases) of a introduced gene
response("/geneCalc?gene=WASH7P")

# Return the names of the genes that are located in the selected parts of the selected chromosomes
response("/geneList?chromo=1&start=0&end=30000")

