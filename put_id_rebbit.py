import pika
from function import conMongo



mongo = conMongo()

queue = "wss_zhuanlihui"
credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(pika.ConnectionParameters("192.168.1.157", 5672, '/', credentials))
channel = connection.channel()
channel.queue_declare(queue=queue, durable=True)

id_number = ['CN%sA' % (j) for j in range(109159000, 110121926)]

for item in id_number[10:-1]:
    print(item)
    channel.basic_publish(exchange='',
                      routing_key= queue,
                      body=item)
print(" [x] Sent 成功")
connection.close()
