#!/usr/bin/python3

# Christian Bermejo Guerrero
# Calculadora REST

import webapp

num1 = None
num2 = None
operacion = None


class calculadoraRest (webapp.webApp):
    """ Calculadora simple con las cuatro operaciones aritmeticas basicas cumpliendo REST
        En esta versión usamos los metodos PUT y GET
        Con PUT actualizamos el estado (ambos operandos a la vez, sino no seria idempotente)
        Con GET obtendremos el resultado de la operacion indicada obviamente sin cambiar el estado
        Los recursos posibles van a ser /suma /resta /multiplicacion y /division """

    def parse(self, request):
        """Return the resource name (including /)"""
        resource = request.split(' ',3)[1]    #nos quedamos con el recurso con la barra
        method = request.split()[0]
        if method == "PUT":
            body = request.split('\r\n\r\n')[-1]
        elif request.split()[0] == "GET":
            body = None
        else: #recibo otra cosa que no sea PUT o GET
            method = "ERROR"

        return (method,resource,body)

    def process(self, resourceName):  #resourceName es lo que antes llamabamos parsedRequest
        """Process the relevant elements of the request."""

        method, resource, body = resourceName
        self.operacion = resource[1:] #quitamos la /
        if (resource == "favicon.ico"):
            httpCode = "404 Not Found"
            htmlBody = "<html><body>Found favicon.ico</body></html>"

        if(method == "PUT"):
            if body != None:
                try:
                    self.num1, self.num2 = body.split(',')
                    if(str.isdigit(self.num1) and str.isdigit(self.num2)):
                        print("op1 = " + self.num1)
                        print("op2 = " + self.num2)

                        print("operacion = " + self.operacion)
                        httpCode = "200 OK"
                        htmlBody = "<html><body>Vamos a calcular la operacion: " \
                                    + str(self.num1) + " " + str(self.operacion) + " " + str(self.num2) \
                                    + "</body></html>"
                    else:
                        httpCode = "200 OK"
                        htmlBody = "<html><body>Has introducido algo mal. Debes introducir /operacion/ seguido de" \
                                    + " dos numeros separados por una coma</body></html>"
                except ValueError:
                    httpCode = "200 OK"
                    htmlBody = "<html><body>Has introducido algo mal. Debes introducir un cuerpo correcto en el PUT</body></html>"

        elif(method == "GET"):
            if(self.operacion == "suma"):
                resultado = int(self.num1) + int(self.num2)
                self.operacion = "+"
            elif(self.operacion == "resta"):
                resultado = int(self.num1) - int(self.num2)
                self.operacion = "-"
            elif(self.operacion == "multiplicacion"):
                resultado = int(self.num1) * int(self.num2)
                self.operacion = "*"
            elif(self.operacion == "division"):
                try:
                    resultado = int(self.num1) / int(self.num2)
                    self.operacion = "/"
                except ZeroDivisionError:
                        httpCode = "HTTP/1.1 200 OK"
                        htmlBody = "<html><body>Error: division entre 0</html></body>"
                        return (httpCode, htmlBody)
            else:
                resultado = "No has introducido una operacion correcta"

            httpCode = "200 OK"
            htmlBody = "<html><body> " + str(self.num1) + str(self.operacion) \
                        + str(self.num2) + " = " + str(resultado)+ "</body></html>"

        return (httpCode,htmlBody)

if __name__ == "__main__":
    testCalcApp = calculadoraRest("localhost",1234)
