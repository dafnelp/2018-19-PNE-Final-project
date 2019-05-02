import http.client
import json

# API information
PORT = 8000
SERVER = 'localhost'


def response(request):

    # Connect to the server
    conn = http.client.HTTPConnection(SERVER, PORT)

    # Send the request.
    conn.request("GET", "/" + request + "&json=1")

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
number = input("Introduce a number of species to show:")
print("The list of species is: ")
response("listSpecies?limit=" + number)

print("The complete list of the species is:")
response("listSpecies?")

specie = input("Introduce a specie:")
response("karyotype?specie=" + specie)

chromo = input("Introduce a chromosome to test:")
response("chromosomeLength?specie=" + specie + "&chromo=" + chromo)

gene = input("Introduce a gene:")
response("geneSeq?gene=" + gene)

response("geneInfo?gene=" + gene)

response("geneCalc?gene=" + gene)

chromo = input("Introduce a chromosome to test:")
start = input("Introduce the starting point:")
end = input("Introduce the endpoint:")
response("geneList?chromo=" + chromo +"&start=" + start + "&end=" + end)

