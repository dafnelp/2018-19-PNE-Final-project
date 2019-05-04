import http.server
import http.client
import socketserver
import termcolor
import json

from Seq import Seq

# This allows that the port does not block
socketserver.TCPServer.allow_reuse_address = True
# Define the port
PORT = 8000


# Class with our handler
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Printing the request line
        termcolor.cprint(self.requestline, 'blue')

        # Dividing the complete request line in order to get the info
        # First having the resource
        comp_request = self.path.split('?')

        # Resource depending the request of the client
        resource = comp_request[0]

        def connection(ENDPOINT):
            """ FUNCTION that will stablish the connection to the ensembl
            data base and will return some info, that will be used later
            PARAMETERS: ENDPOINT --- names given to the resources provided by the server """

            # API information
            HOSTNAME = "rest.ensembl.org"
            METHOD = "GET"

            # Special header in our case is JSON format
            headers = {'content-type': 'application/json'}

            # Connection to the server (ensembl data base)
            conn = http.client.HTTPConnection(HOSTNAME)

            # Send the request
            # Use the defined headers
            conn.request(METHOD, ENDPOINT, "?", headers)

            # Wait for the server's response
            r1 = conn.getresponse()

            # Print the status
            print()
            print("Response received: ", end='')
            print(r1.status, r1.reason)
            print()

            # Read the response's body and close the connection
            text_json = r1.read().decode("utf-8")
            conn.close()

            # Generate the object (species) from the json file
            species = json.loads(text_json)

            # PERFORM THE OPERATIONS DEPENDING THE ENDPOINT

            if "/info/species" in ENDPOINT:

                # Species in the data base
                specie_db = species["species"]

                # Presence of limit parameter
                if "limit" in self.path:
                    # Storing the species as a list
                    common_name = []
                    scientific_name = []
                    # Counter for the species to show
                    counter = 0

                    # Iterate over the list of the information about the species

                    # Establish a counter to show only the species that are selected in the limit input
                    # If this counter is equal to the limit the for loop will break and be only able to show
                    # the species in the counter until that moment
                    for i in specie_db:
                        scientific_name.append(i['name'])  # Key used for the common name of the specie
                        common_name.append(i['display_name'])  # Key used for the scientific name of the specie

                        counter += 1

                        # Only show the species selected
                        if str(counter) == str(limit):
                            break

                        # The program will show the maximum number of species that are in the data base
                        else:
                            continue

                    # Create a list with the common and scientific name of the specie
                    species = [common_name, scientific_name]

                    # --- RETURN --- NAME OF THE SPECIES
                    return species

                # Without the presence of a limit parameter
                else:
                    # Storing the species as a list
                    common_name = []
                    scientific_name = []

                    # Iterate over the list of the information about the species
                    for i in specie_db:
                        scientific_name.append(i['name'])  # Key used for the common name of the specie
                        common_name.append(i['display_name'])  # Key used for the scientific name of the specie

                    # Create a list with the common and scientific name of the specie
                    species = [common_name, scientific_name]

                    # --- RETURN --- NAME OF THE SPECIES
                    return species

            if "/info/assembly/" in ENDPOINT:
                # With this endpoint, we have to return different information
                # depending the request of the client

                if resource == "/karyotype":
                    # This is the key used for the name (usually a number)
                    # of the chromosomes of the specie
                    chromosomes = species["karyotype"]

                    # ---- RETURN --- NAME OF THE CHROMOSOMES
                    return chromosomes

                elif resource == "/chromosomeLength":

                    # Storing the length of the chromosomes as a string
                    len_chromosome = ""

                    # Iterate over the list of the information about the chromosomes
                    # We will only need the length of the chromosome
                    for chromosome in species["top_level_region"]:
                        # The names of the chromosomes must coincide with the chromosome introduced
                        # by the client (chromo)
                        if chromosome["name"] == chromo:  # The key for the name of the chromosomes is "name"
                            len_chromosome = str(chromosome["length"])  # This is the key used for the length

                    # ---- RETURN --- LENGTH OF THE CHROMOSOMES
                    return len_chromosome

            # We have to return the sequence of the gen, so first we need to
            # do the map between the id (ex.ENSG00000165879) and the generic name
            # introduced by the client (ex.FRAT1)

            if "/homology/symbol/human/" in ENDPOINT:
                # With this connection we obtain the id of the introduced gen
                # WE ARE WORKING ONLY WITH HUMAN GENES
                id_gen = species["data"][0]["id"]

                # ---- RETURN --- IDENTIFICATION OF THE GEN
                return id_gen

            if "/sequence/id/" in ENDPOINT:
                seq_gen = species["seq"]

                # ---- RETURN --- SEQUENCE OF THE GENE
                return seq_gen

            if "lookup/id" in ENDPOINT:
                # Different keys for retrieve the information
                start = species["start"]
                end = species["end"]
                id = species["id"]
                chromo_part = species["seq_region_name"]
                # The length of the gene is obtained subtracting the finish and the start position
                length_gene = species["end"] - species["start"]

                # Creating a list wit the information of the gene
                info = [id, chromo_part, start, end, length_gene]

                # ---- RETURN --- INFORMATION ABOUT THE GENE
                return info

            if "overlap/region/human/" in ENDPOINT:
                gene_id = []
                gene_name = []

                for i in range(len(species)):
                    # Gene stable identifier
                    gene_id.append(species[i]["gene_id"])

                    # Symbol of the gene (generic name)
                    gene_name.append(species[i]["external_name"])

                info = [gene_id, gene_name]

                # ---- RETURN --- NAMES OF THE GENE
                return info

        def process_info(f):
            """ Process the info introduced by the client request.
            Parameters:  f: file that should be open depending the request"""

            # Open the file and read the contents
            with open(f, "r") as f:
                content = f.read()

            # Generating the response message
            self.send_response(200)  # --- status line - everything Ok

            # Define the content-type header:
            # In our case text/html (should open an HTML file)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(str.encode(content)))

            # The header is finished
            self.end_headers()

            # Send the response message
            self.wfile.write(str.encode(content))

            return

        def process_error(f):
            """ Process the info introduced by the client request (only if
            the request does not exists).
            Parameters:  f: file that should be open depending the request"""

            # Open the file and read the contents
            with open(f, "r") as f:
                content = f.read()

            # Generating the response message
            self.send_response(404)  # --- status line - file not found error

            # Define the content-type header:
            # In our case text/html (should open an HTML file)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(str.encode(content)))

            # The header is finished
            self.end_headers()

            # Send the response message
            self.wfile.write(str.encode(content))

            return

        def process_json(content):
            # Generating the response message
            self.send_response(200)  # --- status line - everything Ok

            # Define the content-type header:
            # In our case application/jso
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(str.encode(content)))

            # The header is finished
            self.end_headers()

            # Send the response message
            self.wfile.write(str.encode(content))

            return

        # PROCESSING THE DIFFERENT REQUEST OF THE CLIENT

        # Open the main page
        if resource == '/':
            process_info("index.html")

        # Open the page with the message according the request
        elif resource == '/listSpecies':

            # In that case the server creates a json object
            if "json=1" in self.path:
                # Presence of a limit parameter
                if "limit" in self.path:
                    req = comp_request[1].split('&')
                    # Number of species to show
                    limit = req[0][6:]

                    # List of the names of the species
                    names_species = connection("/info/species")
                    # Separate the common and scientific name from the general list
                    cn_species = names_species[0]
                    sn_species = names_species[1]

                    # Now we are going to focus in the number of species to show
                    # In the case that the limit is out of range or the number
                    # is not valid (negative or 0) there will be an error page
                    # If not the selected number of species will be shown or all the
                    # species if the client did not specify a number

                    if limit > "0" and limit <= str(len(cn_species)) or limit == "":
                        # Creating a json object with the requested data
                        process_json(json.dumps({"Common name": cn_species, "Scientific name": sn_species}))

                    else:
                        # The limit selected is out of the range
                        process_error("error-limit.html")

                # Without the presence of a limit parameter
                else:
                    # List of the names of the species
                    names_species = connection("/info/species")
                    # Separates the common and scientific name from the general list
                    cn_species = names_species[0]
                    sn_species = names_species[1]

                    # Creating a json object with the requested data
                    process_json(json.dumps({"Common name": cn_species, "Scientific name": sn_species}))

            # HTML response
            else:
                # Presence of a limit parameter
                if "limit" in self.path:
                    # Number of species to show
                    limit = comp_request[1][6:]

                    # Establish the connection with the data base and
                    # return the info about the species
                    names_species = connection("/info/species")
                    # Separate the common and scientific name from the general list
                    cn_species = names_species[0]
                    sn_species = names_species[1]

                    # A format to presents the species in the HTML, one specie below the other
                    common = ""
                    scientific = ""
                    for i in cn_species:
                        common = common + i
                        common = common + "<br>"
                    for i in sn_species:
                        i = i.replace("_", " ")
                        scientific = scientific + i
                        scientific = scientific + "<br>"

                    if limit > "0" and limit <= str(len(cn_species)) or limit == "":

                        # Open the HTML file in a write mode to write the information
                        # of the page, including the species names
                        f = open("listSpecies.html", "w")

                        f.write("""<!DOCTYPE html>
                        <html lang="en" dir="ltr">
                          <head>
                            <meta charset="utf-8">
                            <title>LIST OF THE SPECIES</title>
                          </head>
                          <body style="background-color: lightsalmon;">
                            <h1 style="color:midnight;">LIST OF THE SPECIES</h1>
                             <h3> The common names are: </h3> 
                             <br>
                             {} 
                             <br>
                             <h3> The scientific names are: </h3> 
                             <br>
                             {}
                             <br>
                             <a href="/"> Back to the main page </a>
                          </body>
                        </html>
                        """.format(common, scientific))

                        # Close the file
                        f.close()

                        # Calling the function to open another page
                        process_info("listSpecies.html")

                    else:
                        # The limit selected is out of the range
                        process_error("error-limit.html")

                # Without the presence of a limit parameter
                else:
                    # Establish the connection with the data base and
                    # return the info about the species
                    names_species = connection("/info/species")
                    # Separates the common and scientific name from the general list
                    cn_species = names_species[0]
                    sn_species = names_species[1]

                    # A format to presents the species in the HTML, one specie below the other
                    common = ""
                    scientific = ""
                    for i in cn_species:
                        common = common + i
                        common = common + "<br>"
                    for i in sn_species:
                        i = i.replace("_", " ")
                        scientific = scientific + i
                        scientific = scientific + "<br>"

                    # Open the HTML file in a write mode to write the information
                    # of the page, including the species names
                    f = open("listSpecies.html", "w")

                    f.write("""<!DOCTYPE html>
                    <html lang="en" dir="ltr">
                      <head>
                        <meta charset="utf-8">
                        <title>LIST OF THE SPECIES</title>
                      </head>
                      <body style="background-color: lightsalmon;">
                        <h1 style="color:midnight;">LIST OF THE SPECIES</h1>
                         <h3> The common names are: </h3> 
                         <br>
                         {} 
                         <br>
                         <h3> The scientific names are: </h3> 
                         <br>
                         {}
                         <br>
                         <a href="/"> Back to the main page </a>
                      </body>
                    </html>
                    """.format(common, scientific))

                    # Close the file
                    f.close()

                    # Calling the function to open another page
                    process_info("listSpecies.html")

        elif resource == "/karyotype":
            # In that case the server creates a json object
            if "json=1" in self.path:
                req = comp_request[1].split('&')
                # Specie introduced by the client
                specie = req[0][7:]

                # Replace the + sign when the specie has two names by _
                # that is the way that appears in ensembl data base
                specie = specie.replace("+", "_").lower()

                try:
                    # Stablish the connection with the data base and
                    # return the info about the karyotype
                    karyotype_specie = connection("/info/assembly/" + specie)

                    # The specie exists in the dat abase but does not have associated any chromosome
                    if karyotype_specie == []:
                        process_error("error-key.html")
                    else:
                        # Creating a json object with the requested data
                        process_json(json.dumps({"chromosomes": karyotype_specie}))

                # In the case the specie does not exist in the data base
                except KeyError:
                    process_error("error-key.html")

            # HTML response
            else:
                # Specie introduced by the client
                specie = comp_request[1][7:]

                # Replace the + sign when the specie has two names by _
                # that is the way that appears in ensembl data base
                specie = specie.replace("+", "_").lower()

                # Stablish the connection with the data base and
                # return the info about the karyotype
                try:
                    karyotype_specie = connection("/info/assembly/" + specie)  # The endpoint needs a parameter (specie)

                    # The specie exists in the dat abase but does not have asociated any chromosome
                    if karyotype_specie == []:
                        process_error("error-key.html")
                    else:
                        # Open the HTML file in a write mode to write the information
                        # of the page, including the karyotype information
                        f = open("karyotype.html", "w")

                        f.write("""<!DOCTYPE html>
                        <html lang="en" dir="ltr">
                          <head>
                            <meta charset="utf-8">
                            <title>KARYOTYPE INFORMATION</title>
                          </head>
                          <body style="background-color: lightsalmon;">
                            <h1 style="color:midnight;">KARYOTYPE INFORMATION</h1>
                             <br> 
                             <h3> The chromosomes of the specie are: </h3> 
                             <br>
                             {}
                             <br>
                             <a href="/"> Back to the main page </a>
                          </body>
                        </html>
                        """.format(karyotype_specie))

                        # Close the file
                        f.close()

                        # Calling the function to open another page
                        process_info("karyotype.html")

                # In case that the specie does not exist in the data base
                except KeyError:
                    process_error("error-key.html")

        elif resource == "/chromosomeLength":
            req = comp_request[1].split('&')
            # Specie introduced by the client
            specie = req[0][7:]
            # Chromosome introduced by the client
            chromo = req[1][7:]
            # Replace the + sign when the specie has two names by _
            # that is the way that appears in ensembl data base
            specie = specie.replace("+", "_").lower()

            # In that case the server creates a json object
            if "json=1" in self.path:
                # Establish the connection with the data base and
                # return the info about the chromosome
                try:
                    chromosome_len = connection("/info/assembly/" + specie)
                    # The specie exists in the dat abase but does not have associated any chromosome
                    if chromosome_len == "":
                        process_error("error-key.html")
                    else:
                        # Creating a json object with the requested data
                        process_json(json.dumps({"length": chromosome_len}))
                except KeyError:
                    process_error("error-key.html")

            # HTML response
            else:
                # Establish the connection with the data base and
                # return the info about the chromosomes
                try:
                    chromosome_len = connection("/info/assembly/" + specie)  # This endpoint needs a parameter (specie)

                    # The specie exists in the dat abase but does not have associated any chromosome
                    if chromosome_len == "":
                        process_error("error-key.html")

                    else:
                        # Open the HTML file in a write mode to write the information
                        # of the page, including the chromosome length
                        f = open("chromosome.html", "w")

                        f.write("""<!DOCTYPE html>
                        <html lang="en" dir="ltr">
                          <head>
                            <meta charset="utf-8">
                            <title>CHROMOSOMES INFORMATION</title>
                          </head>
                          <body style="background-color: lightsalmon;">
                            <h1 style="color:midnight;">CHROMOSOMES INFORMATION</h1>
                             <h3> The length of the introduced chromosome is: </h3>
                             {}
                             <br>
                             <br>
                             <a href="/"> Back to the main page </a>
                          </body>
                        </html>
                        """.format(chromosome_len))

                        # Close the file
                        f.close()

                        # Calling the function to open another page
                        process_info("chromosome.html")

                # In case that the specie does not exist in the data base
                except KeyError:
                    process_error("error-key.html")

        elif resource == "/geneSeq":
            # In that case the server creates a json object
            if "json=1" in self.path:
                req = comp_request[1].split('&')
                # Generic name introduced by the client
                gene = req[0][5:]
                gene = gene.upper()

                # Establish the connection with the data base and first
                # retrieve the id of the introduced gen and then the sequence of the gen
                try:
                    gen_id = connection("/homology/symbol/human/" + gene)  # This endpoint needs a parameter (gene)
                    sequence = connection("/sequence/id/" + gen_id)  # This endpoint needs a parameter (gen_id)
                    # Creating a json object with the requested data
                    process_json(json.dumps({'sequence': sequence}))

                except KeyError:
                    process_error("error-key.html")

            # HTML response
            else:
                gene = comp_request[1][5:]
                gene = gene.upper()

                # Establish the connection with the data base and first
                # retrieve the id of the introduced gen and then the sequence of the gen
                try:
                    gen_id = connection("/homology/symbol/human/" + gene)  # This endpoint needs a parameter (gene)
                    sequence = connection("/sequence/id/" + gen_id)  # This endpoint needs a parameter (gen_id)

                    # Open the HTML file in a write mode to write the information
                    # of the page, including the sequence of the gen.
                    f = open("gen-seq.html", "w")

                    f.write("""<!DOCTYPE html>
                    <html lang="en" dir="ltr">
                      <head>
                        <meta charset="utf-8">
                        <title>GEN SEQUENCE</title>
                      </head>
                      <body style="background-color: lightsalmon;">
                        <h1 style="color:midnight;">GENE SEQUENCE</h1>
                         <h3> The sequence of the gen is: </h3>
                         {}
                         <br>
                         <br>
                         <a href="/"> Back to the main page </a>
                      </body>
                    </html>
                    """.format(sequence))

                    # Close the file
                    f.close()

                    # Calling the function to open another page
                    process_info("gen-seq.html")

                # In case that the specie does not exist in the data base
                except KeyError:
                    process_error("error-key.html")

        elif resource == "/geneInfo":
            # In that case the server creates a json object
            if "json=1" in self.path:
                req = comp_request[1].split('&')
                # Generic name introduced by the client
                gene = req[0][5:]
                gene = gene.upper()

                # Establish the connection with the data base and first
                # retrieve the id of the introduced gen and then the information of the gene
                try:
                    gen_id = connection("/homology/symbol/human/" + gene)  # This endpoint needs a parameter (gene)
                    info_gene = connection("lookup/id/" + gen_id)  # This endpoint needs a parameter (gen_id)
                    # Requested data
                    id = info_gene[0]
                    chromo_part = info_gene[1]
                    start = info_gene[2]
                    end = info_gene[3]
                    length_gene = info_gene[4]
                    info = {"id": id, "chromosome": chromo_part, "start": start, "end": end, "length": length_gene}
                    # Creating a json object with the requested data
                    process_json(json.dumps(info))
                except KeyError:
                    process_error("error-key.html")

            # HTML response
            else:
                # Generic name introduced by the client
                gene = comp_request[1][5:]
                gene = gene.upper()

                # Establish the connection with the data base and first
                # retrieve the id of the introduced gen and then the information of the gene
                try:
                    gen_id = connection("/homology/symbol/human/" + gene)  # This endpoint needs a parameter (gene)
                    info_gene = connection("lookup/id/" + gen_id)  # This endpoint needs a parameter (gen_id)

                    # Requested data
                    id = info_gene[0]
                    chromo_part = info_gene[1]
                    start = info_gene[2]
                    end = info_gene[3]
                    length_gene = info_gene[4]

                    # Open the HTML file in a write mode to write the information
                    # of the page, including the information of the gen.
                    f = open("info-gen.html", "w")

                    f.write("""<!DOCTYPE html>
                    <html lang="en" dir="ltr">
                      <head>
                        <meta charset="utf-8">
                        <title>GENE INFORMATION</title>
                      </head>
                      <body style="background-color: lightsalmon;">
                        <h1 style="color:midnight;">GENE INFORMATION</h1>
                         <h3> ID of the gene: </h3>
                         {} <br>
                         <h3> The chromosome where this gene belongs is: </h3>
                         {} <br>
                         <h3> Start of the gen: </h3>
                         {} <br>
                         <h3> End of the gen: </h3>
                         {} <br>
                         <h3> The length of the gene is: </h3>
                         {} <br>
                         <br>
                         <a href="/"> Back to the main page </a>
                      </body>
                    </html>
                    """.format(id, chromo_part, start, end, length_gene))

                    # Close the file
                    f.close()

                    # Calling the function to open another page
                    process_info("info-gen.html")

                # In case that the specie does not exist in the data base
                except KeyError:
                    process_error("error-key.html")

        elif resource == "/geneCalc":
            # In that case the server creates a json object
            if "json=1" in self.path:
                req = comp_request[1].split('&')
                # Generic name introduced by the client
                gene = req[0][5:]
                gene = gene.upper()
                # Establish the connection with the data base and first
                # retrieve the id of the introduced gen and then the sequence of the gene
                try:
                    gen_id = connection("/homology/symbol/human/" + gene)  # This endpoint needs a parameter (gene)
                    sequence = connection("/sequence/id/" + gen_id)  # This endpoint needs a parameter (gen_id)

                    # Performing the calculations using the class Seq
                    # Obtain the length and the percentage of the bases
                    sequence = Seq(sequence)
                    seq_len = sequence.len()
                    perc_a = sequence.perc("A")
                    perc_t = sequence.perc("T")
                    perc_g = sequence.perc("G")
                    perc_c = sequence.perc("C")
                    info = {"length": seq_len, "A percentage ": perc_a, "T percentage": perc_t, "G percentage": perc_g, "C percentage": perc_c}
                    # Creating a json object with the requested data
                    process_json(json.dumps(info))

                except KeyError:
                    process_error("error-key.html")
            # HTML response
            else:
                # Generic name introduced by the client
                gene = comp_request[1][5:]
                gene = gene.upper()

                # Establish the connection with the data base and first
                # retrieve the id of the introduced gen and then the sequence of the gene
                try:
                    gen_id = connection("/homology/symbol/human/" + gene)  # This endpoint needs a parameter (gene)
                    sequence = connection("/sequence/id/" + gen_id)  # This endpoint needs a parameter (gen_id)

                    # Performing the calculations using the class Seq
                    # Obtain the length and the percentage of the bases
                    sequence = Seq(sequence)
                    seq_len = sequence.len()
                    perc_a = sequence.perc("A")
                    perc_t = sequence.perc("T")
                    perc_g = sequence.perc("G")
                    perc_c = sequence.perc("C")

                    # Open the HTML file in a write mode to write the information
                    # of the page, including the sequence of the gen.
                    f = open("cal-gen.html", "w")

                    f.write("""<!DOCTYPE html>
                    <html lang="en" dir="ltr">
                      <head>
                        <meta charset="utf-8">
                        <title>GENE CALCULATIONS</title>
                      </head>
                      <body style="background-color: lightsalmon;">
                        <h1 style="color:midnight;">GENE CALCULATIONS</h1>
                         <h3> The length of the sequence is: </h3>
                         {} <br>
                         <h3> The percentage of A bases is: </h3>
                         {} <br>
                         <h3> The percentage of C bases is: </h3> 
                         {} <br>
                         <h3> The percentage of T bases is: </h3> 
                         {} <br>
                         <h3> The percentage of G bases is: </h3>
                         {} <br>
                         <br>
                         <a href="/"> Back to the main page </a>
                      </body>
                    </html>
                    """.format(seq_len, perc_a, perc_c, perc_t, perc_g))

                    # Close the file
                    f.close()

                    # Calling the function to open another page
                    process_info("cal-gen.html")

                # In case that the specie does not exist in the data base
                except KeyError:
                    process_error("error-key.html")

        elif resource == "/geneList":
            # In that case the request message have different parts
            req = comp_request[1].split('&')
            # Chromosome introduced by the client
            chromo = str(req[0][7:])
            # Start position of the chromosome
            start = str(req[1][6:])
            # End position of the chromosome
            end = str(req[2][4:])

            # In that case the server creates a json object
            if "json=1" in self.path:
                # Establish the connection with the data base and retrieve the
                # genes of the selected part of the  chromosome
                try:
                    genes_id = connection("overlap/region/human/" + chromo + ":" + start + "-" + end + "?feature=gene")
                    # Requested info
                    gene_id = genes_id[0]
                    gene_name = genes_id[1]
                    # The client have introduced valid numbers of the chromosome and the start and end point
                    # but they do not correspond to any gene in the data base
                    if gene_id == [] or gene_name == []:
                        process_error("error.html")
                    else:
                        # Creating a json object with the requested data
                        process_json(json.dumps({"id": gene_id, "name": gene_name}))

                except KeyError:
                    process_error("error-key.html")

            # HTML response
            else:
                # Establish the connection with the data base and retrieve the
                # genes of the selected part of the  chromosome
                try:
                    # This endpoint needs three parameters (chromo, start, end)
                    # We also have to introduced the type of feature to retrieve,
                    # in our case gene, nevertheless multiple values are accepted
                    genes_id = connection("overlap/region/human/" + chromo + ":" + start + "-" + end + "?feature=gene")

                    #Requested info
                    gene_id = genes_id[0]
                    gene_name = genes_id[1]
                    # A format to presents the species in the HTML, one specie below the other
                    id = ""
                    name = ""
                    for i in gene_id:
                        id = id + i
                        id = id + "<br>"
                    for i in gene_name:
                        name = name + i
                        name = name + "<br>"

                    # The client have introduced valid numbers of the chromosome and the start and end point
                    # but they do not correspond to any gene in the data base
                    if gene_id == [] or gene_name == []:
                        process_error("error.html")

                    # In this case everything is correct
                    else:
                        # Open the HTML file in a write mode to write the information
                        # of the page, including the names of the genes.
                        f = open("genes-chromo.html", "w")

                        f.write("""<!DOCTYPE html>
                        <html lang="en" dir="ltr">
                          <head>
                            <meta charset="utf-8">
                            <title>GENE NAMES</title>
                          </head>
                          <body style="background-color: lightsalmon;">
                            <h1 style="color:midnight;">GENE NAMES</h1>
                             <h3>The id of the genes are: </h3>
                             {} <br>
                             <h3>The names of the genes are: </h3>
                             {} <br>
                             <br>
                             <a href="/"> Back to the main page </a>
                          </body>
                        </html>
                        """.format(id, name))

                        # Close the file
                        f.close()

                        # Calling the function to open another page
                        process_info("genes-chromo.html")

                except KeyError:
                    process_error("error-key.html")

        # Error page
        else:
            process_error("error.html")


# MAIN PROGRAM

with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
    socketserver.TCPServer.allow_reuse_address = True
    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- client, the handler is called
    try:
        httpd.serve_forever()

    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()

print("")
print("Server Stopped")
