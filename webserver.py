from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import cgi

# IMPORT CRUD OPERATIONS

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

###############################################################

# MODULES FOR PYTHON 3

# from urllib.parse import parse_qs
# from http.server import HTTPServer, BaseHTTPRequestHandler

##############################################################

# Connect to the Restaurants SQL database

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/restaurants'):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()

                output = ''
                output += '<html><body>'
                output += "<a href='/restaurants/new'>Add new restaurant</a></br></br>"

                for restaurant in restaurants:
                    output += restaurant.name
                    output += '</br>'
                    output += "<a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
                    output += '</br>'
                    output += "<a href='/restaurants/%s/delete'>Delete</a>" %restaurant.id
                    output += '</br>'
                    output += '</br>'

                output += '</body></html>'

                self.wfile.write(output)
                return
            
            if self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
            
                output = ''
                output += '<html><body>'
                output += "<form method='POST' action='/restaurants/new' enctype='multipart/form-data'>"
                output += "<input name='newRestaurantName' placeholder='New Restaurant Name' type='text'><input type='submit' value='Add'></form> "
                output += '</body></html>'
                self.wfile.write(output)
                return

            if self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                
                output = ''
                output += '<html><body>'
                output += '<h2> Okay, how about this: </h2>' 

                output += "<form method='POST' action='/hello' enctype='multipart/form-data'><h2>What would you like me to say?</h2>"
                output += "<input name='message' placeholder='message' type='text'><input type='submit' value='submit'></form>"
                output += '</body></html>'

                self.wfile.write(output)
                return

            if self.path.endswith('/edit'):
                restaurantIDPath = self.path.split('/')[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('content-type', 'text/html')
                    self.end_headers()

                    output = ''
                    output += '<html><body>'
                    output += '<h1>'
                    output += myRestaurantQuery.name
                    output += '</h1>'                    
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurantIDPath
                    output += "<input name='newRestaurantName' type='text' placeholder='%s' >" % myRestaurantQuery.name
                    output += "<input type='submit' value='Rename'>"
                    output += '</form>'
                    output += '</html></body>'

                    self.wfile.write(output)
            

            if self.path.endswith('/delete'):
                restaurantIDPath = self.path.split('/')[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('content-type', 'text/html')
                    self.end_headers()

                    output = ''
                    output += '<html><body>'
                    output += "<h1>Are you sure you want to delete %s?</h1>" % myRestaurantQuery.name                 
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurantIDPath
                    output += "<input type='submit' value='Delete'>"
                    output += '</form>'
                    output += '</html></body>'

                    self.wfile.write(output)

       
            if self.path.endswith('/hola'):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                
                output = ''
                output += '<html><body>'
                output += '<h2> Okay, how about this: </h2>' 

                output += "<form method='POST' action='/hello' enctype='multipart/form-data'><h2>What would you like me to say?</h2>"
                output += "<input name='message' placeholder='message' type='text'><input type='submit' value='submit'></form>"
                output += '</body></html>'

                self.wfile.write(output)
                return
        except IOError:
            self.send_error(404, 'File not found %s' % self.path)

    def do_POST(self):
        try:
            # self.send_response(301)
            # self.end_headers()
            
            # ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            # if ctype == 'multipart/form-data':
            #     fields = cgi.parse_multipart(self.rfile, pdict)
            #     messagecontent = fields.get('message')
            
        # URLLIB    
            
            # length = int(self.headers.get('Content-length'))
            # body = self.rfile.read(length).decode()
            # params = parse_qs(body)
            # messagecontent = params["message"][0]
        

            # output = ''
            # output += '<html><body>'
            # output += '<h2> Okay, how about this: </h2>' 
            # output += '<h1> %s </h2>' % messagecontent[0]

            # output += "<form method='POST' action='/hello' enctype='multipart/form-data' ><h2>What would you like me to say?</h2>"
            # output += "<input name='message' placeholder='message' type='text'><input type='submit' value='submit'></form>"
            # output += '</body></html>'
            # self.wfile.write(output)

            if self.path.endswith('/edit'):
          
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                print(ctype)
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split('/')[2]

                    myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                    print(myRestaurantQuery)

                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-Type' , 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith('/delete'):
               
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                restaurantIDPath = self.path.split('/')[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()

                if myRestaurantQuery != []:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-Type' , 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()


            if self.path.endswith('/restaurants/new'):        
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                

                newRestaurant = Restaurant(name = messagecontent[0])
                session.add(newRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()



        except:
            pass




def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print('Server running on port %s' % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print('Stopping web server...')
        server.socket.close()

if __name__ == '__main__':
    main()

