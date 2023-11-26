Usage Sample
''''''''''''

.. code:: python

   from cf import CollFilter

   if __name__ == '__main__':
       data = read_data(train_path)
       data = pre_process(data)  # return [(user_id: Any, item_id: Any, float),]
       cf = CollFilter(data)
       ucf = cf.user_cf()  # return {user_id: [(item_id, score),],}
       icf = cf.item_cf()  # return {user_id: [(item_id, score),],}
       cf.release()

