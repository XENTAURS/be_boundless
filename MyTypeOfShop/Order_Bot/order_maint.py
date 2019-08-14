#!/usr/bin/python
#
# This script connects to the MySQL database and deletes all orders created by the Order Bot once an hour
# Prerequisites:
#   pip install mysql-connector-python
#

import mysql.connector
from mysql.connector import errorcode
import datetime
import sys
import os
import time

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("/root/shopizer-automate/logs/order_maint.log", "a",0)

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass

if __name__ == '__main__':


    if not os.path.exists('/root/shopizer-automate/logs'):
        os.mkdir('/root/shopizer-automate/logs')

    sys.stdout = Logger()

    while True:

        dt = datetime.datetime.now().strftime('%m-%d-%y %H:%M:%S')
        print('\n' + '--------------- {0} ---------------'.format(dt) + '\n')

        try:
          print('Connecting to MySQL server 10.20.19.106...')
          cnx = mysql.connector.connect(user='shopizer', password='C1sc0.123',
                                          host='10.20.19.106',
                                          database='SALESMANAGER')
          if cnx.is_connected():
              print('Connected to MySQL server!')
          cursor = cnx.cursor()
          sql_query_orders = ("select ORDER_ID from ORDERS where BILLING_LAST_NAME = 'Bot'")
          print('Querying orders to delete.')
          cursor.execute(sql_query_orders)
          order_ids = [x[0] for x in cursor.fetchall()]
          print('Order IDs to be deleted: {0}'.format(order_ids))

          for order_id in order_ids:
              sql_delete_order_total = "delete from ORDER_TOTAL where ORDER_ID = {0}".format(order_id)
              sql_delete_sm_transaction = "delete from SM_TRANSACTION where ORDER_ID = {0}".format(order_id)
              sql_delete_order_product_price = "delete from ORDER_PRODUCT_PRICE where ORDER_PRODUCT_ID = {0}".format(order_id)
              sql_delete_order_product = "delete from ORDER_PRODUCT where ORDER_ID = {0}".format(order_id)
              sql_delete_order_status = "delete from ORDER_STATUS_HISTORY where ORDER_ID = {0}".format(order_id)
              sql_delete_order = "delete from ORDERS where ORDER_ID = {0}".format(order_id)
              sql_delete_customer = "delete from CUSTOMER where CUSTOMER_ID = {0}".format(order_id)

              cursor.execute(sql_delete_order_total)
              cursor.execute(sql_delete_sm_transaction)
              cursor.execute(sql_delete_order_product_price)
              cursor.execute(sql_delete_order_product)
              cursor.execute(sql_delete_order_status)
              cursor.execute(sql_delete_order)
              cursor.execute(sql_delete_customer)
              cnx.commit()
              print('Deleted order with Order_ID {0}'.format(order_id))
          print('Going to sleep for 1hr.  Good night.')
          time.sleep(3600)

        except mysql.connector.Error as err:
          if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
          elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
          else:
            print(err)
        finally:
            if(cnx.is_connected()):
                cnx.close()
                print("Closing connection to MySQL server")


