from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models.user import User
from app.models.post import Post

class UserModelCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_password_hashing(self):
        u = User(username='test_password', email='tessssst@gmail.com')
        u.set_password('cat')
        
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))
    
    def test_follow(self):
        u1 = User(username='Vin', email='vin_venture@gmail.com')
        u2 = User(username='Elend', email='elend_venture@gmail.com')

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u2.followed.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'Elend')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'Vin')
        
        u1.unfollow(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        u1 = User(username='Vin', email='vin_venture@gmail.com')
        u2 = User(username='Elend', email='elend_venture@gmail.com')
        u3 = User(username='Kelsier', email='kelsier@gmail.com')
        u4 = User(username='Sazed', email='sazed@gmail.com')

        now = datetime.utcnow()
        post1 = Post(body='Vin, The heir of the Survivor and Empress of Luthade; Mistborn', 
        author=u1, timestamp = now + timedelta(seconds=1))
        post2 = Post(body='Elend, the Emperor of Luthadel; Mistborn',
        author=u2, timestamp= now + timedelta(seconds=4))
        post3= Post(body='Kelsier, the Survivor of Hathesin; Mistborn',
        author=u3, timestamp= now + timedelta(seconds=3))
        post4 = Post(body='Sazed, the Hero of Ages; Keeper of Terris',
        author=u4, timestamp=now + timedelta(seconds=2))

        db.session.add_all([u1,u2,u3,u4])
        db.session.add_all([post1,post2,post3,post4])
        db.session.commit()

        u1.follow(u2)
        u1.follow(u3)
        u2.follow(u1)
        u4.follow(u1)
        u4.follow(u2)
        u4.follow(u3)

        f1 = u1.get_followed_posts().all()   
        f2 = u2.get_followed_posts().all()
        f3 = u3.get_followed_posts().all()
        f4 = u4.get_followed_posts().all()    

        self.assertEqual(f1, [post2, post3, post1])
        self.assertEqual(f2, [post2, post1])
        self.assertEqual(f3, [post3])
        self.assertEqual(f4, [post2, post3, post4, post1]) 

if __name__ == '__main__':
    unittest.main(verbosity=2)

