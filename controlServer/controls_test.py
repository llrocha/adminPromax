import unittest
from controls import BaseControls
from controls import ApacheControls
from controls import DataBaseControls
from controls import BuildBotControls
from controls import EnvironControls
from controls import JobsControls
from controls import ServerControls


class BaseControlsTest(unittest.TestCase):
    def test_geos(self):
        bc = BaseControls('')
        self.assertTrue('Sem geografias disponíveis!' == bc.status())

    def test_instances(self):
        bc = BaseControls('')
        self.assertTrue(len(bc.instances()) == 0)


class ApacheControlsTest(unittest.TestCase):
    def test_start(self):
        ap = ApacheControls()
        ap.stop()
        pre = ap.status()
        ap.start()
        actual = ap.status()
        self.assertFalse(pre == actual)

    def test_stop(self):
        ap = ApacheControls()
        ap.start()
        pre = ap.status()
        ap.stop()
        actual = ap.status()
        self.assertFalse(pre == actual)

    
        
if __name__ == '__main__':
    unittest.main()


#ap = ApacheControls()
# bb = BuildBotControls()
# db = DataBaseControls()
# en = EnvironControls()
# jb = JobsControls()


#print(ap.geos)
# print(bb.geos)
# print(db.geos)
# print(en.geos)
# print(jb.geos)


#print(ap.status())
# print(bb.status())
# print(db.status())
# print(en.status())
# print(jb.status())


#ap.start()
#ap.status()
#ap.stop()
#ap.status()