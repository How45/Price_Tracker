import unittest
import helper as hp

class TestApp(unittest.TestCase):
    """
    Unit testing class
    """

    def test_new(self):
        """
        Test when user presses 1
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
        # link_list = ['www.2', 'www.']
        item_name = ['test1', 'test2']
        # file_name = 'Pcs'
        price_list = [[9.2,10.5],[10.2,11.5]]
        date = [['09/08/23','10/08/23'],['09/08/23','10/08/23']]
        hp.draw_graph(price_list, item_name, date)

if __name__ == '__main__':
    unittest.main()
