import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import jwt
import sys
import json

'''
make sure that the secret key is symmetric among the app server and the chat server otherwise the auth wont work
''' 
key = "thisisasecretkey123"

def checkOnlineStatus(self,listOfFriends):
    #the listoffriends is a string with comma separated friend emails
    listofOnlineFriends =[]
    list1=listOfFriends.split(',') #convert the string to array

    #store the list of friends of each user
    self.friends_list = list1

    print ("printing array list1 ")
    for i in list1:
        print i

    print ("total list of friends sent by user: " + listOfFriends)

    for c in WSHandler.clients:
            print "c user online " + c._current_user

            if c._current_user in list1:

                listofOnlineFriends.append(c._current_user)
                print "friend online " + c._current_user

                packet = {"msgFrom" : "SERVER_ADMIN",
                            "msgText" : "",
                            "msgType" : "status_update_singleClient",
                            "status"  : "online",
                           "friendEmail" : self._current_user}
                string_packet = json.dumps(packet)  #convert json packet to string before sending it to client        
                c.write_message(string_packet)
                
    
    #now send the listofOnlineFriends to the new user
    print ("Current user is " + self._current_user)
    packet = {"msgFrom" : "SERVER_ADMIN",
              "msgType" : "online_status_list",
              "friendList" : listofOnlineFriends}
    string_packet = json.dumps(packet)  #convert json packet to string before sending it to client        
    self.write_message(string_packet)
    return



class WSHandler(tornado.websocket.WebSocketHandler):
    clients = []
    client_emails = {}  #this dictionary keeps track of number of active sockets per user/email. Incase multiple sessions are alive then we need to keep track of how many sockets are there for each user

    def open(self):
        print 'new connection'
        token = self.get_argument('token')
        print "got a get request. This is the value of the token %s" % (token,)
        print "creating an empty friends list on connection open"
        self.friends_list= []
        
        decoded = {}
        try:
            print "trying to decode the JWT received"
            decoded = jwt.decode(token, key, algorithms='HS256')
        except:
            print "Token verification failed. Closing the socket"
            self._current_user= "404_BAD_USER_404"
            self.close(400, "bad authentication token")

            #return
        else:
            print decoded["issuedTo"].encode('UTF-8')
            self._current_user = decoded["issuedTo"].encode('UTF-8')
            print "setting the _current_user"

            #currUser= self.current_user()
            print "The curr user returned is " + self._current_user
            print "saving the current user and its websocket in the list"
            
            WSHandler.clients.append(self)
            
            #if user/email is not in dict then add it with value of 1
            #if user/email is in dict then simply increment value

            if not self._current_user in WSHandler.client_emails:
                WSHandler.client_emails[self._current_user] = 1
            else:
                WSHandler.client_emails[self._current_user] += 1
            
    

    def on_message(self, message):
        print 'string message received:  %s' % message
        
	
    	parsed_json = json.loads(message)
        msgType = parsed_json['msgType']

        if(msgType == "checkOnlineStatus"):
            checkOnlineStatus(self,parsed_json['listOfFriends'])
            return

    	print ("the msg type is: " + msgType)
        msg= parsed_json['text']
    	
        print ("the text is: " + msg)
        
        msgTo = parsed_json['msgTo']

        print ("the message is for : " + msgTo)

        client_online = False
	    
        # Reverse Message and send it back
        #print 'sending back message: %s' % message
	    #print (message["text"])
        #self.write_message("Send you the same message back:" + message)
        for c in WSHandler.clients:
            print "print users online " + c._current_user
            if c._current_user == msgTo:
                print "found the client online"
                
                client_online = True
                
                packet = {"msgFrom" : self._current_user,
                            "msgType" : "message",
                           "msgText" : msg}
                string_packet = json.dumps(packet)  #convert json packet to string before sending it to client        
                c.write_message(string_packet)
                
                '''if we return now then only the first socket with that user email will be sent the msg. In case client 
                has opened multiple tabs (hence there will be multiple sockets for the same client email) 
                then only 1 tab gets the reply back if we return. If we dont return and let it loop
                through all the online clients then we get to server all the tabs opened for the same client
                '''
                #return  
        if(client_online == True):
            return
        else:            
            print "client is not online"
            packet = {"msgFrom" : "SERVER_ADMIN",
                       "msgType" : "error",
                       "msgText" : "The client is not online"}
            string_packet = json.dumps(packet)  #convert json packet to string before sending it to client           
            self.write_message(string_packet)
            return    

    def on_close(self):
        print 'connection closed and removing client+ws from active clients list'
        print 'updating all online friends (of client) that client is going offline'

        '''
        if multiple connections are opened then we dont inform other clients of offline status
        until it is the last connection/socket that is going down
        
        '''
        if(self._current_user == "404_BAD_USER_404"):
            print "BAD USER 404. closing connection"
            return

        if(WSHandler.client_emails[self._current_user] > 1):
            
            WSHandler.client_emails[self._current_user] -= 1
            
            WSHandler.clients.remove(self)
            return

        #else if its the last/only conn/socket then tell the users friends that he is going offline
        else: 

            for c in WSHandler.clients:
            #print "print users online " + c._current_user
                if c._current_user in self.friends_list :
                    #print "found the client online"

                    packet = {"msgFrom" : "SERVER_ADMIN",
                                "msgText" : "",
                                "msgType" : "status_update_singleClient",
                                "status"  : "offline",
                               "friendEmail" : self._current_user}
                    string_packet = json.dumps(packet)  #convert json packet to string before sending it to client        
                    c.write_message(string_packet)
                    
            del WSHandler.client_emails[self._current_user] #delete key/user email from dict since its the last occurence         
            WSHandler.clients.remove(self)
            return
 
    





    def check_origin(self, origin):
        return True
 
application = tornado.web.Application([
    (r'/ws*', WSHandler),
])
 
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = "127.0.0.1"
    print '*** Websocket Server Started at %s***' % myIP
    tornado.ioloop.IOLoop.instance().start()
