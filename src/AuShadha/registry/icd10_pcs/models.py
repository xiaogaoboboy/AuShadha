###############################################################
# PROJECT: AuShadha ICD10 Procedure Code Models
# Author : Dr. Easwar T R
# Date   : 28-08-2012
# Licence: GNU GPL V3. Please see AuShadha/LICENSE.txt
################################################################


from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms

from django.contrib.auth.models import User
from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel


from AuShadha.apps.clinic.models import Clinic


# ICD10 PROCEDURE CODE MODELS ############################################


class RootXML(models.Model):
   
    """
      The RootXML file for ICD10PCS model. 
      This is left here just because the parser outputs this model. 
      Will have to change it in the parser before I remove it here
    """
    __model_label__ = 'root_xml'

    index = models.PositiveIntegerField(max_length = 200, unique= True)
    fk = models.CharField(max_length = 30, null = True, blank = True)
    path = models.CharField(max_length = 100)

    def __unicode__(self):
        return "%s: @ %s" % (self.path, self.index)
    
    def get_unique_section_labels(self):
        all_tables = PcsTable.objects.all()
        system_list = []
        for i, table in enumerate(all_tables):
            axis = Axis.objects.filter(pcsTable_fk = table)
            section_label_obj = Label.objects.filter(fk = axis[0])
            section_label = section_label_obj[0].text
            if not section_label in system_list:
                system_list.append(section_label)
        return section_list



class PcsTable(models.Model):

    """
      The ICD10 pcsTable model.

    """

    __model_label__ = "pcs_table"

    index = models.PositiveIntegerField(max_length = 200, unique = True)
    fk = models.ForeignKey(RootXML, null=True,blank =True)
    
    def _get_name(self, name):
        label_map = {'section': 0, 'body_system': 1, 'operation': 2}
        try:
         label_index = label_map[name]
        except KeyError:
         raise Exception("Invalid Name key")

        id = self.id
        table_obj = PcsTable.objects.get(pk= id)
        axis = Axis.objects.filter(pcsTable_fk = table_obj)
        label_obj = Label.objects.filter(fk = axis[label_index])
        label = label_obj[0].text
        if label == 'None' or label is None:
           return None, label_obj
        return label, label_obj


    def get_section_name(self):
       return self._get_name('section')[0]

    def get_body_system_name(self):
       return self._get_name('body_system')[0]

    def get_operation_name(self):
       return self._get_name('operation')[0]

    def get_table_name(self):
        return "%s :%s :%s" %(self.get_section_name(), 
                            self.get_body_system_name(), 
                            self.get_operation_name()
                      )

    def get_section(self):
        return self._get_name('section')[1]

    def get_body_system(self):
        return self._get_name('body_system')[1]

    def get_operation(self):
        return self._get_name('operation')[1]

    def __unicode__(self):
        return self.get_table_name()



class PcsRow(models.Model):

    """
      The ICD10 pcsRow model.

    """

    __model_label__ = "pcs_row"

    index = models.PositiveIntegerField(max_length = 200, unique = True)
    fk = models.ForeignKey(PcsTable,null=True,blank=True)
    
    def __unicode__(self):
        return "%s" % (self.index)
    
        


class Axis(models.Model):

    """
      The ICD10 Axis model.

    """

    __model_label__ = "axis"

    index = models.PositiveIntegerField(max_length = 200, unique = True)
    positions = models.CharField(max_length = 30, null = True, blank = True)
    values = models.CharField(max_length = 30, null = True, blank=True)
    pcsTable_fk = models.ForeignKey(PcsTable,null=True,blank=True)
    pcsRow_fk = models.ForeignKey(PcsRow,null=True,blank=True)
   
    def __unicode__(self):
        return "%s %s %s" % (self.index, self.positions, self.values)

    


class Title(models.Model):

    """
      The ICD10 Title model.

    """

    __model_label__ = "title"

    index = models.PositiveIntegerField(max_length = 200, unique = True)
    text = models.TextField(max_length = 1000, null = True, blank = True)
    fk = models.ForeignKey(Axis,null=True,blank=True)
    
    def __unicode__(self):
        return "%s %s" % (self.index, self.text)

   


class Label(models.Model):

    """
      The ICD10 Label model.

    """

    __model_label__ = "label"

    index = models.PositiveIntegerField(max_length = 200, unique = True)
    text = models.TextField(max_length = 1000, null = True, blank = True)
    code = models.CharField(max_length = 100, null = True, blank=True)
    fk = models.ForeignKey(Axis,null=True,blank=True)

    def __unicode__(self):
        return "%s %s %s" % (self.index, self.text, self.code)


class Definition(models.Model):
 
    """
      The ICD10 Definition  model.

    """

    __model_label__ = "definition"

    index = models.PositiveIntegerField(max_length = 200, unique = True)
    text = models.TextField(max_length = 1000, null = True, blank = True)
    fk = models.ForeignKey(Axis,null=True,blank=True)

    def __unicode__(self):
        return "%s %s" % (self.index, self.text)
