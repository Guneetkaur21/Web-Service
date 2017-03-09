import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['gexf'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
	send_from_directory(app.config['UPLOAD_FOLDER'],
	                               filename)
	import networkx as nx
	import matplotlib.pyplot as plt
	from xml.dom import minidom
	from collections import OrderedDict
	from xml.dom.minidom import parse, parseString

	
	g=nx.read_gexf(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	nx.draw(g)
	node_type = nx.get_node_attributes(g,'Node Type')
	node_subType =nx.get_node_attributes(g,'Node Subtype')
	node_time=nx.get_node_attributes(g,'Expected Time Spent')
	node_score=nx.get_node_attributes(g,'Maximum Score')
	node_content=nx.get_node_attributes(g,'Content Type')



	listData = []  

	for p in node_time.keys():
	    if(p in node_score.keys()):
	        if(p in node_content.keys()):
	            if(p in node_subType.keys()):
	                if(p in node_type.keys()):
	                    NodesWithValues=(p,node_type.get(p),node_subType.get(p),node_time.get(p),node_score.get(p),node_content.get(p))
	                    
	                    
	                 
	Ids_values={}                    #dict of ids as keys
	for k in node_type.keys():
	    if(k in node_subType.keys()):
	        Ids_values[k]=(node_subType.get(k),node_type.get(k))

	for k in Ids_values.keys():
	    t0,t1 = Ids_values.get(k)
	    if(k in node_time.keys()):
	        t2=node_time.get(k)
	        Ids_values[k]=(t0,t1,t2)
	    else:
	        Ids_values[k]=(t0,t1,None)

	for k in Ids_values.keys():
	    t0,t1,t2 = Ids_values.get(k)
	    if(k in node_score.keys()):
	        t3=node_score.get(k)
	        Ids_values[k]=(t0,t1,t2,t3)
	    else:
	        Ids_values[k]=(t0,t1,t2,None)

	for k in Ids_values.keys():
	    t0,t1,t2,t3 = Ids_values.get(k)
	    if(k in node_content.keys()):

	        t4=node_content.get(k)
	        Ids_values[k]=(t0,t1,t2,t3,t4)
	    else:
	        Ids_values[k]=(t0,t1,t2,t3,None)


	#for n in Ids_values:
	#    print "%s = %s \n"%(n,nodes1[n])


	doc = parse(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	listoflists=[]
	Ids_labels = {}              #dict of ids as keys and labels as values
	nlabel = []
	nid = []

	nodes = doc.getElementsByTagName("node")

	for node in nodes:
	    nnlabel=node.getAttribute("label")
	    nnid=node.getAttribute("id")
	    nlabel.append(nnlabel)
	    nid.append(nnid)
	    #print ("labels:%s ids:%s"%
	     #      (nlabel , nid))

	for i in range(len(nid)):
	    if(nid[i] in nid):
	        Ids_labels[nid[i]]=(nlabel[i])
	    else:
	        Ids_labels[i]=(nid[i],None)
	    

	#for n in nodes2:
	#    print "%s = %s \n"%(n,nodes2[n])


	from collections import defaultdict
	d1 = defaultdict(list)
	nsource=[]
	ntarget=[]
	listoflist=[]

	edges = doc.getElementsByTagName("edge")

	for edge in edges:
	    nnsource = edge.getAttribute("source")
	    nntarget = edge.getAttribute("target")
	    nsource.append(nnsource)
	    ntarget.append(nntarget)
	    #listoflist.append((list(nsource), list(ntarget))
	temp=[]
	n=1
	ntarget.append(n)
	        
	TargetsAndSources_Ids={}                  #dict of targets and sources as ids
	for i in range(len(ntarget)-1):
	    if(ntarget[i]==ntarget[i+1]):
	            temp.append(nsource[i])
	            #n3[ntarget[i]]=(temp[i+1])
	            i=i+1
	    else:
	            temp.append(nsource[i])
	            TargetsAndSources_Ids[ntarget[i]]=temp
	           
	            temp = []
	           

	# for d in TargetsAndSources_Ids:
	#     print "%s = %s \n"%(d,TargetsAndSources_Ids[d])




	TargetsAndSources_labels = {}        #targets as keys and sources as values

	for i in range(len(TargetsAndSources_Ids.keys())):
	    target_id = TargetsAndSources_Ids.keys()[i]
	    for l in range(len(Ids_labels.keys())):
	        node_id = Ids_labels.keys()[l]
	        if target_id == node_id:
	            target_lab = Ids_labels.values()[l]
	            for j in range(len(TargetsAndSources_Ids.values()[i])):
	                arr = []
	                for t in TargetsAndSources_Ids.values()[i]:
	                    edge_val = t 
	                   
	                    for k in range(len(Ids_labels.keys())):
	                        node_i = Ids_labels.keys()[k]
	                        
	                        if edge_val == node_i:
	                            
	                            arr.append(Ids_labels.values()[k])
	            TargetsAndSources_labels[target_lab] = arr

	#for all the nodes which are not there in targets
	NodesNotInTargets_Ids=[]

	for i in range(len(Ids_values.keys())):                 #to get the ids
	    node_key=Ids_values.keys()[i]
	    if node_key not in TargetsAndSources_Ids.keys():
	            NodesNotInTargets_Ids.append(node_key)
	    
	#print NodesNotInTargets_Ids

	NodesNotInTargets_labels=[]                         #to get the labels
	for i in range(len(NodesNotInTargets_Ids)):
	    temp_val=NodesNotInTargets_Ids[i]
	    for j in range(len(Ids_labels)):
	        node_id=Ids_labels.keys()[j]
	        if(temp_val==node_id):
	            NodesNotInTargets_labels.append(Ids_labels.values()[j])
	           

	#for all the nodes which are not there in edges values

	NodesNotInSources_Ids=[]                 #to get the ids
	for i in range(len(Ids_values.keys())):
	    k=0
	    node_key=Ids_values.keys()[i]
	    for j in TargetsAndSources_Ids.values():
	        if node_key not in j:
	            k=k+1
	    if k==len(TargetsAndSources_Ids.keys()):
	        NodesNotInSources_Ids.append(node_key)
	        
	#print NodesNotInSources_Ids

	NodesNotInSources_labels=[]              #to get the labels
	for i in range(len(NodesNotInSources_Ids)):
	    temp_val=NodesNotInSources_Ids[i]
	    for j in range(len(Ids_labels)):
	        node_id=Ids_labels.keys()[j]
	        if(temp_val==node_id):
	            NodesNotInSources_labels.append(Ids_labels.values()[j])
	            

	#for nodes not in targets and sources both
	NodesNotInTargetsAndSources= NodesNotInSources_labels + NodesNotInSources_labels

	            

	#to find all the sources which are not targets using recurssion
	source=[]
	def recurrence(p):
	    for n in p:
	        if n not in TargetsAndSources_Ids.keys():
	            source.append(n)
	        elif n in range(len(TargetsAndSources_Ids.keys())):
	            if n not in source:
	                rec(TargetsAndSources_Ids.keys()[n].values())

	    return source


	for i in range(len(TargetsAndSources_Ids.values())):
	    node_val=TargetsAndSources_Ids.values()[i]
	    SourcesNotTargets = recurrence(node_val)
	    
	SourcesNotTargets_labels=[]              #to get the labels
	for i in range(len(SourcesNotTargets)):
	    temp_val=SourcesNotTargets[i]
	    for j in range(len(Ids_labels)):
	        node_id=Ids_labels.keys()[j]
	        if(temp_val==node_id):
	            SourcesNotTargets_labels.append(Ids_labels.values()[j])
	            
	            

	TargetsAlsoSources={}                 #targets which are also in sources
	for i in range(len(TargetsAndSources_labels)):
	    target_id=TargetsAndSources_labels.keys()[i]
	    for j in range(len(TargetsAndSources_labels.values())):
	        target_val=TargetsAndSources_labels.values()[j]
	        if target_id in target_val:
	            value=TargetsAndSources_labels.values()[i]
	            TargetsAlsoSources[target_id]=value
	            
	#print TargetsAlsoSources


	NodesOnlyTargets={}                  #Nodes that are only targets
	for i in range(len(TargetsAndSources_labels)):
	    target_id=TargetsAndSources_labels.keys()[i]
	    k=0
	    for j in range(len(TargetsAndSources_labels.values())):
	        target_val=TargetsAndSources_labels.values()[j]
	        if target_id not in target_val:
	            k=k+1
	    if(k==len(TargetsAndSources_labels.keys())):     
	        value=TargetsAndSources_labels.values()[i]
	        NodesOnlyTargets[target_id]=value
	            
	#print NodesOnlyTargets
	            

	            
	# print NodesNotInSources_string          
	# print       
	# print NodesNotInTargets_string    
	# print    
	# print SourcesNotTargets_string            
	# print            
	# #print TargetsAndSources_labels   
	# ''.join('{}{} | '.format(key, val) for key, val in TargetAndSources_labels.items())

	for i in range(len(NodesNotInTargetsAndSources)):
	    NodesNotInTargetsAndSources_string="["+ NodesNotInTargetsAndSources[i]+"]"
	    #print NodesNotInTargetsAndSources_string,



	NodesNotInTargets_list=[]
	for i in range(len(NodesNotInTargets_labels)):
	    string="["+ NodesNotInTargets_labels[i]+"]"
	    NodesNotInTargets_list.append(string)
	    
	NodesNotInTargets_string="".join(NodesNotInTargets_list)
	    



	#for getting a string of targets which are also sources    
	TargetsAlsoSources_string=""
	TargetsAlsoSources_list=[]
	for k,v in TargetsAlsoSources.items():
	    myString="".join(k)
	    myString2=":".join(v)
	    string=("["+myString +"|"+myString2+"]")
	    TargetsAlsoSources_list.append(string)
	TargetsAlsoSources_string="".join(TargetsAlsoSources_list) 



	#for getting the targets which are only nodes
	NodesOnlyTargets_string=""
	NodesOnlyTargets_list=[]
	for k,v in NodesOnlyTargets.items():
	    myString="".join(k)
	    myString2=":".join(v)
	    #print myString2
	    #for i in myString2:
	    
	    string=("["+myString +"|"+myString2+"]")
	    NodesOnlyTargets_list.append(string)
	    
	NodesOnlyTargets_string="".join(NodesOnlyTargets_list) 

	FinalString="".join(NodesNotInTargets_list)+"".join(NodesOnlyTargets_list)+"".join(TargetsAlsoSources_list) 

	# print NodesNotInTargets_string
	# print TargetsAlsoSources_string
	# print NodesOnlyTargets_string
	return FinalString





if __name__ == '__main__':
   app.run(debug = True)