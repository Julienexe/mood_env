from django.db import models
from mood_trackers.models import User
from PIL import Image


class Profile(models.Model):
    
    #mood choices to set the different moods for each user
    class Moods(models.TextChoices):
        HAPPY ='happy','Happy'
        SAD ='sad','Sad'
        ANGRY ='angry','Angry'
        CONFUSED ='confused','Confused'
        FEARFUL ='fearful','Fearful'
        DISGUSTED ='disgusted','Disgusted'
        LOW_SELF_ESTEEM ='low_self_esteem','Low Self Esteem'
        INSPIRED ='inspired','Inspired'
        JOYFUL ='joyful','Joyful'
        ENTHUSIASTIC ='enthusiastic','Enthusiastic'
        HIGH_SELF_ESTEEM ='high_self_esteem','High Self Esteem'
        GRATEFUL ='grateful','Gratified'
        AMAZINGLY_GOOD ='amazingly good','Amazingly Good'
        GOOD ='good','Good'
        NEUTRAL ='neutral','Neutral'
        BAD ='bad','Bad'
        RELATIONSHIPS ='relationships','Relationships'
        LIFELESSNESS ='lifelessness','Lifelessness'
        DEPRESSION ='depression','Depression'
        PAIN ='pain','Pain'
        SHAME ='shame','Shame'
        GUILT ='guilt','Guilt'
        FRUSTRATION ='frustration','Frustration'
        TENSE ='tense','Tense'
        IRRITATED ='irritated','Irritated'
        BOREDOM ='boredom','Boredom'
        WORRY ='worried','Worried'
        INSECURITY ='insecurity','Insecurity'
        ADHD = 'ADHD', 'ADHD'
        ANXIETY = 'anxiety', 'Anxiety'

    #user roles to distinguish therapists from normal users
    class Roles(models.TextChoices):
        CLIENT = 'client','Client'
        THERAPIST = 'therapist','Therapist'    

    mood = models.CharField(max_length=100, choices = Moods.choices, default=Moods.NEUTRAL)

    role = models.CharField(max_length=25, choices=Roles.choices, default=Roles.CLIENT)

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) #always add the null, db_constraint and blank fields to avoid getting IntegrityErrors

    avatar = models.ImageField(
        default='avatar.jpg', # default avatar
        upload_to='profile_avatars' # dir to store the image
    )

    def __str__(self):
        return f'{self.user.name} Profile'

    def save(self, *args, **kwargs):
        # save the profile first
        super().save(*args, **kwargs)

        # resize the image
        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            # create a thumbnail
            img.thumbnail(output_size)
            # overwrite the larger image
            img.save(self.avatar.path)

            #tuple?