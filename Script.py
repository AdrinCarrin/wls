import constantes

def createJMSModule(jms_module_name):
	cd('/')
	cmo.createJMSSystemResource(jms_module_name)
	cd('/JMSSystemResources/'+jms_module_name)
	set('Targets',jarray.array([ObjectName('com.bea:Name='+constantes.SERVER_NAME+',Type='+constantes.SERVER_TYPE)], ObjectName))

def getJMSModulePath(jms_module_name):
	jms_module_path='/JMSSystemResources/'+jms_module_name+"/JMSResource/"+jms_module_name
	print jms_module_path
	return jms_module_path

def createJMSConnectionFactory(jms_module_name, jms_cf_name, jms_cf_jndi):
	jms_module_path=getJMSModulePath(jms_module_name)
	cd(jms_module_path)
	
	cmo.createConnectionFactory(jms_cf_name)
	
	jms_cf_path = jms_module_path+'/ConnectionFactories/'+jms_cf_name
	
	cd(jms_cf_path)
	cmo.setJNDIName(jms_cf_jndi)
	
	cd(jms_cf_path+'/SecurityParams/'+jms_cf_name)
	cmo.setAttachJMSXUserId(false)
	
	cd(jms_cf_path+'/ClientParams/'+jms_cf_name)
	cmo.setClientIdPolicy('Restricted')
	cmo.setSubscriptionSharingPolicy('Exclusive')
	cmo.setMessagesMaximum(10)
	
	cd(jms_cf_path+'/TransactionParams/'+jms_cf_name)
	cmo.setXAConnectionFactoryEnabled(true)
	
	cd(jms_cf_path+'/')
	cmo.setDefaultTargetingEnabled(true)
	
	
def createJMSUDQ(jms_module_name, jms_udq_name, jms_udq_jndi, type):
	jms_module_path=getJMSModulePath(jms_module_name)
	cd(jms_module_path)
	cmo.createUniformDistributedQueue(jms_udq_name)

	cd('/JMSSystemResources/'+jms_module_name+'/JMSResource/'+jms_module_name+'/UniformDistributedQueues/'+jms_udq_name)
	cmo.setJNDIName(jms_udq_jndi)
	cmo.setDefaultTargetingEnabled(true)

def createJMSUDT(jms_module_name, jms_udt_name, jms_udt_jndi):
	jms_module_path=getJMSModulePath(jms_module_name)

	cd('/JMSSystemResources/'+jms_module_name+'/JMSResource/'+jms_module_name)
	cmo.createUniformDistributedTopic(jms_udt_name)

	cd('/JMSSystemResources/'+jms_module_name+'/JMSResource/'+jms_module_name+'/UniformDistributedTopics/'+jms_udt_name)
	cmo.setJNDIName(jms_udt_jndi)
	cmo.setForwardingPolicy('Replicated')
	cmo.setDefaultTargetingEnabled(true)


def createQueue(jms_module_name, jms_queue_name, jms_jdni):
	jms_module_path=getJMSModulePath(jms_module_name)
	cd(jms_module_path)
	cmo.createUniformDistributedQueue(jms_queue_name)

	cd('/JMSSystemResources/'+jms_module_name+'/JMSResource/'+jms_module_name+'/Queues/'+jms_queue_name)
	cmo.setJNDIName(jms_jndi)
	cmo.setDefaultTargetingEnabled(true)
	
def createTopic(jms_module_name, jms_topic_name, jms_jdni):
	jms_module_path=getJMSModulePath(jms_module_name)
	cd(jms_module_path)
	cmo.createUniformDistributedQueue(jms_topic_name)

	cd('/JMSSystemResources/'+jms_module_name+'/JMSResource/'+jms_module_name+'/Queues/'+jms_topic_name)
	cmo.setJNDIName(jms_jndi)
	cmo.setDefaultTargetingEnabled(true)
	
	
def setErrorQueue(jms_module_name, jms_name, jms_error_queue)
	jms_type = getJMSType(jms_name)
	cd('/JMSSystemResources/'+jms_module_name+'/JMSResource/'+jms_module_name+'/'+jms_type+'/'+jms_name+'/DeliveryFailureParams/'+jms_name)
	cmo.setErrorDestination(getMBean('/JMSSystemResources/'+jms_module_name+'/JMSResource/'+jms_module_name+'/'+jms_type+'/'+jms_error_queue))

def getJMSType(jms_resource):
	cd('/JMSSystemResources/my_module2/JMSResource/my_module2')
	if jms_resource in str(cmo.getConnectionFactories()):
		return "ConnectionFactories"
	if jms_resource in str(cmo.getQueues()):
		return "Queues"
	if jms_resource in str(cmo.getTopics()):
		return "Topics"
	if jms_resource in str(cmo.getDistributedQueues()):
		return "DistributedQueues"
	if jms_resource in str(cmo.getDistributedTopics()):
		return "DistributedTopics"
	if jms_resource in str(cmo.getUniformDistributedQueues()):
		return "UniformDistributedQueues"
	if jms_resource in str(cmo.getUniformDistributedTopics()):
		return "UniformDistributedTopics"	
	
#Begin
#jms_module_name = "MODULE_NAME"
connect(constantes.ADMIN_USER, constantes.ADMIN_PASSWORD, constantes.ADMIN_URL)

edit()
startEdit()

try:
	createJMSModule(jms_module_name)
	#createJMSConnectionFactory(jms_module_name,'new_jms_cf','new.jms.cf')
	
	createTopic(jms_module_name,'eis/wls/Topic1','eis.wls.topic1')
	createQueue(jms_module_name,'eis/wls/Queue1','eis.wls.queue1')
	createJMSUDQ(jms_module_name,'eis/wls/Udq1','eis.wls.Udq1')
	createJMSUDT(jms_module_name,'eis/wls/Udt1','eis.wls.Udt1')
	
	save()
	activate()
except:
	print "EXCEPTION OCURRED"
	undo()
	raise

