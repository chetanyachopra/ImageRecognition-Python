import tensorflow as tf,sys
image_path=sys.argv[1]

#read image data
image_data=tf.gfile.FastGFile(image_path,'rb').read()

#loads label file,strips off cariage return 

label_lines=[line.rstrip() for line in tf.gfile.GFile(r'C:\Users\CHETANYA\tf_files\retrained_labels.txt')]

#unpersists graph from file 
with tf.gfile.FastGFile(r'C:\Users\CHETANYA\tf_files\retrained_graph.pb',"rb") as f:
	graph_def=tf.GraphDef()
	graph_def.ParseFromString(f.read())
	_=tf.import_graph_def(graph_def,name='')


with tf.Session() as sess:
	softmax_tensor=sess.graph.get_tensor_by_name('final_result:0')

	predictions=sess.run(softmax_tensor,{'DecodeJpeg/contents:0': image_data})
	top_k=predictions[0].argsort()[-len(predictions[0]):][::-1]

	for node_id in top_k:
		human_string=label_lines[node_id]
		score=predictions[0][node_id]
		print('%s (score=%.5f)' % (human_string,score))

# python C:\Users\CHETANYA\tf_files\tell.py C:\Users\CHETANYA\tf_files\objects\chair\c.jpg