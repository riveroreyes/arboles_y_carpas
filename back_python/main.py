from flask import Flask, request, url_for, render_template, jsonify
from flask_cors import CORS
from itertools import combinations
import requests, json, itertools
from pprint import pprint

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#----------------------------------------------------------------------------------------------------
#Llamada a proceso desde api
@app.route('/api/procesar_lista', methods=["POST"])
def procesar_lista():
	
	if not request.json:
		return jsonify( {"error":"Tipos de datos incorrectos"} )

	data = json.loads( request.data  )

	print(data)

	dimension = data['dimension']
	if dimension < 6 or dimension > 200:
		return jsonify( {"error":"El ancho del puzzle debe estar entre 6 y 200"} )

	v1 = leer_procesar_validar( dimension , [], True)
	return jsonify(v1)

#----------------------------------------------------------------------------------------------------
#Ejecutar proceso de lectura, proceso y validacion del puzzle
def leer_procesar_validar( dimension , errores = [], isJson = False  ):

	r,mensaje = '',''
	resp,cols,rows,lista = [],[],[],[]

	#leer los datos
	r = requests.get('http://www.leafnoisepracticas.ml/api/map?s={}'.format(dimension) )

	datos = r.json()

	resp = datos['map']['data']
	cols = datos['map']['cols']
	rows = datos['map']['rows']

	resp = [[0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0], [0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0], [0, 2, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0], [0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0], [0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0], [2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]] 
	cols = [4, 3, 3, 2, 2, 5, 0, 4, 3, 2, 4, 1, 1, 4, 1, 4, 1, 4, 3, 3] 
	rows= [3, 2, 5, 2, 1, 4, 3, 1, 4, 2, 3, 2, 3, 1, 6, 0, 4, 0, 7, 1] 

	print('\n\nresp =',resp,'\ncols =', cols,'\nrows=',rows,'\n\n')

	#Trasponer filas con columnas, y aumentar en n+1, n+1 la matrix
	lista = [ [1]+list(x)+[1] for x in zip(*resp) ]

	row_adic = [ 1 for elem in range( len(resp)+2  ) ] #Fila adicional a agregar al inicio y final llena de unos: [1,1,1,1,...1]
	lista.insert(0,row_adic)
	lista.append(row_adic)

	cols = [0]+cols+[0]
	rows = [0]+rows+[0]

	#descartar las columnas que poseen solo arena y arboles
	for pos, valor in enumerate(cols):
		if valor == 0:
			for x in range( len(lista) ) :
				if lista[x][pos] == 0:
					lista[x][pos] = 1

	#descartar las filas que poseen solo arena y arboles
	lambda1 = lambda y:1 if y==0 else y
	lambda2 = lambda row,el: list( map( lambda1  , el) )   if row == 0 else el
	lista = list( map( lambda2, rows ,lista)  )

	#transformar todas las celdas en hierbas que no tienen un arbol en su vertical u horizontal. 
	for x in range( len(lista) ):
		for y in range( len(lista) ):
			if lista[x][y] == 0 and lista[x-1][y] != 2 and lista[x+1][y] != 2 and lista[x][y-1] != 2  and lista[x][y+1] != 2:
				lista[x][y] = 1 

	lista = asignarCarpasEnFilas(lista, rows, cols) 	#asignar las carpas por fila que sean inequivocas
	lista = asignarCarpasEnColumnas(lista, rows, cols) 	#asignar las carpas por columna que sean inequivocas
	lista = asignarCarpasInequivocas(lista, rows, cols) #asignar carpas a arboles que solo tengan un campo en vacio que sean inequivocas

	if dimension <= 30:
		lista = ejecutarEnsayoYError(lista, rows, cols) 

	#Eliminar las filas y columnas agregadas para el analisis y preparar la validacion
	resp = list( map( lambda x:list( map( lambda y:y ,x[1:-1] ) ) , lista[1:-1]  )  )

	#ENVIAR DATOS A VALIDACION
	r = requests.post('http://www.leafnoisepracticas.ml/api/map', json = 
		{
			"data":list( map( lambda x: list(x), zip(*resp) ) ), #trasponer para enviar
			"cols":cols[1:-1],
			"rows":rows[1:-1]
		})			

	mensaje_validacion = ''
	validado = False

	if r.status_code == requests.codes.ok:
		
		respuesta = r.json()
		print('\n\n',respuesta)
		
		if respuesta['valid'] == False:
			mensaje_validacion = 'NO PUDO SER VALIDADO. Verifique e intente de nuevo'
			errores.append( {'resp':resp, 'cols':cols[1:-1], 'rows':rows[1:-1] } )
		else:
			mensaje_validacion = 'VALIDACION EXITOSA!'
			validado = True

	else:
		mensaje_validacion	+= '. Codigo de estado:  {}'.format(r.status_code)

	if isJson:
		return {
			"resp":resp,
			"cols":cols[1:-1],
			"rows":rows[1:-1],
			"valid":validado
		}

#----------------------------------------------------------------------------------------------------
#manejar los errores de las paginas
@app.errorhandler(404)
def pagina_de_error(error):
	return 'Pagina no existe', 404

#----------------------------------------------------------------------------------------------------
#asignar las carpas por fila que sean inequivocas
def asignarCarpasEnFilas(lista, rows, cols):

	for x in range( len(lista)  ):
		unosYTres = 0
		tres = 0
		for y in range( len(lista) ):
			if lista[x][y] == 0 or lista[x][y] == 3: #verificar que la suma de vacios y arboles sea igual a lo indicado en la fila
				unosYTres = unosYTres + 1

			if lista[x][y] == 3: 
				tres = tres + 1

		if rows[x] > 0:  
			if  unosYTres  == rows[x]:
				for y in range( 1, len(lista)-1 ):
					if lista[x][y] == 0:
						lista[x][y] = 3 # es una carpa

						rodearDeArenaCarpa(lista, x, y, rows, cols, False)
						break
			elif tres == rows[x]:
				for y in range( len(lista) ):
					if lista[x][y] == 0:
						lista[x][y] = 1

	return lista
	
#----------------------------------------------------------------------------------------------------
#asignar las carpas por columna que sean inequivocas
def asignarCarpasEnColumnas(lista, rows, cols):
	for y in range( len(lista) ):
		a = [row[y] for row in lista] #obtener la columna
		
		if cols[y] > 0:
			if ( a.count(0) + a.count(3) ) == cols[y]:
				#procesar todas las columnas
				for m in range( 0, len(lista) ):
					for n in range( y, y+1 ):
						if lista[m][n] == 0:
							lista[m][n] = 3 # es una carpa
							
							rodearDeArenaCarpa(lista,m,n, rows, cols, False)
							break
			elif a.count(3) == cols[y]:
				#procesar todas las columnas
				for m in range( 0, len(lista) ):
					for n in range( y, y+1 ):
						if lista[m][n] == 0:
							lista[m][n] = 1

	return lista

#----------------------------------------------------------------------------------------------------
#Rodear de arena la carpa. Si soloArena es true, indica que se llenaran para verificar casos de probabilidad
def rodearDeArenaCarpa(lista, m, p, rows, cols, soloArena):

	posTotal = [ [m-1,p-1],	[m-1,p], [m-1,p+1],	[m,p-1], [m,p+1], [m+1,p-1], [m+1,p], [m+1,p+1] ]
	for k in posTotal:
		if lista[ k[0] ][ k[1] ] == 0:
			lista[ k[0] ][ k[1] ] = 1

	if soloArena == False:
		lista = asignarCarpasEnFilas(lista, rows, cols) 
		lista = asignarCarpasEnColumnas(lista, rows, cols)
		lista = asignarCarpasInequivocas(lista, rows, cols) 
	
	return lista

#----------------------------------------------------------------------------------------------------
#Probar celdas aleatoreamente para ver si da un resultado posible
#Devuelve 1 para todo Ok, 0 para no es correcto y -1 para todas las posiciones revisadas
def ensayoYError(lista, rows, cols, posicionesTotalesRevisadas, filaInicio, columnaInicio):

	boolTodoRevisado = 1;
	posiciones = []

	for x in range( filaInicio, len(lista)-1 ):
		for y in range( columnaInicio, len(lista)-1 ):
			if lista[x][y] == 0:
				
				if posiciones.count( [x,y] ) == 0 and posicionesTotalesRevisadas.count( [x,y] ) == 0 :

					lista[x][y] = 3 # es una carpa

					if 	verificarTodoOk(lista, rows, cols) == -1:
						lista[x][y] = 0 #devuelvo, no procede dentro de los limites de cols y rows
						continue

					posiciones.append([x,y])
					
					if len(posiciones) == 1:
						posicionesTotalesRevisadas.append([x,y]) #voy acumulando en el total

					boolTodoRevisado = 0

					rodearDeArenaCarpa(lista, x, y, rows, cols, False)

	verificar = verificarTodoOk(lista, rows, cols)

	if verificar == 1:
		return 1

	if boolTodoRevisado == 1:
		return -1

	return 0

#----------------------------------------------------------------------------------------------------
#Verifica que coincidan los arboles por filas y columnas con los datos dados en cols y roes
#return -1 es que las carpas superan lo permitido. return 0 es que son diferentes pero menores
def verificarTodoOk(lista, rows, cols):

	#validar que cda fila este completa
	for x, filas in enumerate(lista):
		if filas.count(3) > rows[x]:
			return -1
		elif rows[x] !=  filas.count(3):
			return 0

	#validar que cada columna este completa
	for y in range(1, len(lista)-1):
		a = [row[y] for row in lista] #obtener la columna
		if a.count(3) > cols[y]:
			return -1
		elif a.count(3) != cols[y]:
			return 0

	#validar que cada arbol no este solo o no hay una carpa junta
	if isArbolSolo(lista) or isCarpaJunta(lista):
		print('ARBOL SOLO o CARPA JUNTA')
		return -1

	#llenar el resto con hierbas
	lista = list( map( lambda x: list(map( lambda y:1 if y==0 else y  ,x ))    , lista) )

	return 1 # todo ok

#----------------------------------------------------------------------------------------------------
#asignar carpas inequivocas
def asignarCarpasInequivocas(lista, rows, cols):

	largoEx = len(lista);

	for x in range(0, largoEx ):

		for y in range(0 , largoEx ):
		
			if lista[x][y] == 2:

				pos = [	 [x-1,y],	[x+1,y],	[x,y-1],	[x,y+1] 	]

				arr = []
				for k in pos:
					arr.append( lista[ k[0] ][ k[1] ]  )

				#si la cantidad de ceros es uno y no tenga carpas asignadas
				if arr.count( 0 ) == 1 and arr.count(3) == 0:
					lista[ pos[arr.index(0)][0] ][ pos[arr.index(0)][1]  ] = 3 #es una carpa
					#De inmediato todo lo que rodea la carpa que no sea arbol es arena.
					#Tomo la posicion de la carpa
					m = pos[arr.index(0)][0]
					p = pos[arr.index(0)][1] 
					
					rodearDeArenaCarpa(lista,m,p, rows, cols, False )

	lista = asignarCarpasEnFilas(lista, rows, cols ) 
	lista = asignarCarpasEnColumnas(lista, rows, cols)

	return lista

#----------------------------------------------------------------------------------------------------
#Ensayo y error con celdas hasta determinar la primera respuesta correcta
def ejecutarEnsayoYError(lista, rows, cols):

	#conseguir conbinaciones de columnas posibles
	history = dict()

	getCombinacionesColumnas( lista, rows, cols );

	return lista

#----------------------------------------------------------------------------------------------------
# Obtener el contenido numerico de un valor alfanumerico
def get_num_from_string(string):  
	num = ''  
	for i in string:  
		if i in '1234567890':  
			num+=i  
	integer = int(num)  
	return integer  

#----------------------------------------------------------------------------------------------------
# Obtener las combinaciones n! / m! (n-m)!, de un array numerado 0... hasta n
def getTodosLosGrupos(elementos, conjuntos):
	result = []
	for pareja in combinations(elementos, conjuntos):
		a = []
		a.append(pareja)
		result.append( list(itertools.chain.from_iterable(a))  ) #llevar tupla a array

	return result

#----------------------------------------------------------------------------------------------------
# Determinar las combinaciones de las filas y columnas.
def getCombinacionesFilasColumnas(lista, rows, cols):

	resRow, resCol = [],[]
	# Determinar la relacion en las filas entre carpas a colocar, carpas colocadas y espacios disponibles 
	for i,fila in enumerate(lista, start=0):
		if i > 0 and i < len(lista)-1:
			if rows[i] > 0:
				resRow.append( [ 'f{}'.format(i-1), 	fila.count(0) - ( rows[i] - fila.count(3) ), rows[i] - fila.count(3) ] )

	# Determinar la relacion en las columnas entre carpas a colocar, carpas colocadas y espacios disponibles 
	for y in range(1, len(lista)-1):
		columna = [row[y] for row in lista] 
		if cols[y] > 0:  
			resCol.append( [ 'c{}'.format(y-1), columna.count(0) - ( cols[y] - columna.count(3) ), cols[y] - columna.count(3) ])


	arr = []
	for x in resRow:
		for y in resCol:
			arr.append(	getCombinacionesXY( lista, [x,y] )	)

	return arr

#----------------------------------------------------------------------------------------------------
# Determinar las combinaciones de las columnas.
def getCombinacionesColumnas(lista, rows, cols):

	resCol = []
	combinaciones = dict()
	# Determinar la relacion en las columnas entre carpas a colocar, carpas colocadas y espacios disponibles 
	for y in range(1, len(lista)-1):
		columna = [row[y] for row in lista] 
		if cols[y] > 0:  
			resCol.append( [ 
				y-1, #pos columna
				cols[y], #lo que se pide
				columna.count(0), #cantidad de ceros mas las carpas
				columna.count(3), #cantidad de arboles
				])

			result = []
			for pareja in combinations( posiciones , cols[y] - columna.count(3) ): # [1,2,3] (m) para formar grupos de m
				result.append( pareja ) #llevar tupla a array

		combinaciones[str(y)] = result

	print(resCol)
	pprint(combinaciones)


	'''
	arr = []
	for x in resRow:
		for y in resCol:
			arr.append(	getCombinacionesXY( lista, [x,y] )	)
	return arr
	'''


#----------------------------------------------------------------------------------------------------
def getCombinacionesXY( lista, resultado ):

	posibilidadesTotales = []

	for data in resultado:

		pos = get_num_from_string( data[0] ) # Extraer le valor numerico de fn o cn: f10 o c4, creado previamente
		universo =  data[1] + data[2] # Determina el universo de ceros: n
		elementos =  data[2] # Determina el valor de: m, para la conbinacion n! / m! (n-m)!
		probables = []

		if data[0].find('f') == 0:
			#Si son filas
			for x in range( pos+1, pos+2 ):
				for y in range( 1, len(lista)-1 ):
					if lista[x][y] == 0:
						probables.append( [x,y] )
		else:
			#Si son columnas
			for x in range( 1, len(lista)-1 ):
				for y in range( pos+1, pos+2 ):
					if lista[x][y] == 0:
						probables.append( [x,y] )

		posibilidades = []

		r = getTodosLosGrupos( list( range( 0, universo  ) ), elementos ) # Seleccionar los subconjuntos, se envia un consecutivo desde el cero hasta el numero de parejas
		
		arr1 = list( map( lambda x: list( map( lambda y: probables[y], x  ) )  , r )  ) # asociar las posiciones con los puntos x,y probables

		posibilidadesTotales.append( arr1 )


	enviar = []

	if len(posibilidadesTotales) == 1:
		enviar = posibilidadesTotales[0]
	else:
		enviar = posibilidadesTotales[0]
		for i in range( 1, len(posibilidadesTotales) ):
			enviar =  [(c + p) for c in enviar for p in posibilidadesTotales[i]] #producto cartesiano en sumas.

	return enviar

#----------------------------------------------------------------------------------------------------
#Analizar todas las posiciones alrededor para determinar cual arbol esta libre y marcarlo
def isArbolSolo(lista):

	for x in range(len(lista)):
		for y in range(len(lista)):
			if lista[x][y] == 2:
				if lista[x-1][y] != 3 and	lista[x+1][y] != 3 and	lista[x][y-1] != 3 and	lista[x][y+1] != 3:
					return True

	return False

#----------------------------------------------------------------------------------------------------
#Analizar todas las posiciones alrededor para determinar cual arbol esta libre y marcarlo
def isCarpaJunta(lista):

	for m in range(len(lista)):
		for p in range(len(lista)):
			if lista[m][p] == 3:
				posTotal = [ [m-1,p-1],	[m-1,p], [m-1,p+1],	[m,p-1], [m,p+1], [m+1,p-1], [m+1,p], [m+1,p+1] ]
				for k in posTotal:
					if lista[ k[0] ][ k[1] ] == 3:
						return True

	return False

#----------------------------------------------------------------------------------------------------
#proceso masivo
def procesoMasivo(dimension, mapas):

	errores = []
	for i in range(0,mapas):
		print( 'Mapa: {}'.format(i+1) )
		leer_procesar_validar( dimension , errores )

	print('ERRORES: ',end='')
	if len(errores) == 0:
		print('NO HAY ERRORES'	)
	else:
		print('LOS SIGUIENTES SON ERRORES'	)
		print(errores)

#----------------------------------------------------------------------------------------------------
#Determina si la carpa a colocar para la probabilidades esta sola y es posible colocarla
def isPosibleColocarCarpaSola(lista, m, p):

	posTotal = [ [m-1,p-1],	[m-1,p], [m-1,p+1],	[m,p-1], [m,p+1], [m+1,p-1], [m+1,p], [m+1,p+1] ]
	for k in posTotal:
		if lista[ k[0] ][ k[1] ] == 3:
			return False

	return True

#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	app.run('0.0.0.0',5000,debug=True)