def is_FormDataField_filled(data):
   if data == None:
      return False
   if data == '':
      return False
   if data == []:
      return False
   return True