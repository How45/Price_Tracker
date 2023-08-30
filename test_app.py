"""testing module to test code"""
import unittest
import helper as hp
import sql_commands as sql

class TestApp(unittest.TestCase):
    """
    Unit testing class
    """
    def test_initialise(self):
        """
        Test inserting data
        """
        link_list = ['www.3', 'www.4']
        item_name = ['test1', 'test2']
        file_name = 'Tvs'
        price_list = [100.2,11.2]
        date = ['29-08-2023','29-08-2023']

        hp.initialise_data_graph(link_list, price_list, file_name, item_name, date)


    def test_drawgraph(self):
        """
        Test draw_graph
        """
        # link_list = ['www.2', 'www.']
        item_name = ['test1', 'test2']
        # file_name = 'Pcs'
        price_list = [9.2,10.2]
        date = ['09/08/23','09/08/23']
        hp.draw_graph(price_list, item_name, date)


    def test_load(self):
        """
        Test when user presses 2
        """
        hp.load('Pcs')


    def test_getdata(self):
        """
        Test on retrieving data
        """
        print(sql.get_attributes('Pcs'))

    def test_getlink(self):
        """
        Test on retrieving Links
        """
        link_id = sql.get_link_id('Pcs')
        print(tuple(link_id),type(tuple(link_id)))


if __name__ == '__main__':
    unittest.main()
