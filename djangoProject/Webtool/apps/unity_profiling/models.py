# -*- coding: utf-8 -*-
from django.db import models

class SceneModel(models.Model):
    scene_pic = models.ImageField(upload_to = 'unity_profiling_pic')
    project_name=models.CharField(max_length=50)
    scene_name = models.CharField(max_length=50)
    scene_des = models.CharField(max_length=100)
    date_time=models.CharField(max_length=50)