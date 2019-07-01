import logging
from io import BytesIO
import os
import xml.dom.minidom
import requests
import time

from settings import APPLICATION_ID, APPLICATION_PASSWORD
from upload_file import get_blob, upload_blob


class ProcessingSettings:
    Language = "English"
    OutputFormat = "xml"


class Task:
   Status = "Unknown"
   Id = None
   DownloadUrl = None

   def is_active(self):
      if self.Status == "InProgress" or self.Status == "Queued":
         return True
      else:
         return False


class AbbyyOnlineSdk:
   ServerUrl = "https://cloud-eu.ocrsdk.com/"

   ApplicationId = APPLICATION_ID
   Password = APPLICATION_PASSWORD
   Proxies = {}

   def process_image(self, image_data, settings):
      request_url = self.get_request_url("processMRZ")

      url_params = {
          "language": settings.Language,
          "exportFormat": settings.OutputFormat,
          "profile": "textExtraction",
          "imageSource": "scanner"
      }

      image_data.seek(0)
      content = image_data.read()
      response = requests.post(
          request_url,
          data=content, #params=url_params,
          auth=(self.ApplicationId, self.Password),
          proxies=self.Proxies)

      # Any response other than HTTP 200 means error - in this case exception will be thrown
      response.raise_for_status()

      # parse response xml and extract task ID
      task = self.decode_response(response.text)
      return task

   def get_task_status(self, task):
      if task.Id.find('00000000-0') != -1:
         # GUID_NULL is being passed. This may be caused by a logical error in the calling code
         print("Null task id passed")
         return None

      url_params = {"taskId": task.Id}
      status_url = self.get_request_url("getTaskStatus")

      response = requests.get(status_url, params=url_params,
                        auth=(self.ApplicationId, self.Password), proxies=self.Proxies)
      task = self.decode_response(response.text)
      return task

   def download_result(self, task, output_path):
      get_result_url = task.DownloadUrl
      if get_result_url is None:
         print("No download URL found")
         return
      print(get_result_url)
      file_response = requests.get(get_result_url, stream=True, proxies=self.Proxies)
      string_obj = BytesIO()
      string_obj.write(file_response.content)
      string_obj.seek(0)
      upload_blob(output_path, string_obj)
      return file_response.content

   def decode_response(self, xml_response):
      """ Decode xml response of the server. Return Task object """
      dom = xml.dom.minidom.parseString(xml_response)
      task_node = dom.getElementsByTagName("task")[0]
      task = Task()
      task.Id = task_node.getAttribute("id")
      task.Status = task_node.getAttribute("status")
      if task.Status == "Completed":
         task.DownloadUrl = task_node.getAttribute("resultUrl")
      return task

   def get_request_url(self, url):
      return self.ServerUrl.strip('/') + '/' + url.strip('/')
   

# Recognize a file at filePath and save result to resultFilePath
def _recognize_file(image_data, result_file_path, language, output_format):
    print("Uploading..")
    settings = ProcessingSettings()
    settings.Language = language
    settings.OutputFormat = output_format
    task = AbbyyOnlineSdk().process_image(image_data, settings)

    if task is None:
        print("Error")
        return

    if task.Status == "NotEnoughCredits":
        print("Not enough credits to process the document. Please add more pages to your application's account.")
        return


    print("Id = {}".format(task.Id))
    print("Status = {}".format(task.Status))
    # Wait for the task to be completed
    print("Waiting..")
    while task.is_active():
        time.sleep(0.5)
        print(".")
        task = AbbyyOnlineSdk().get_task_status(task)

    print("Status = {}".format(task.Status))
    if task.Status == "Completed":
        if task.DownloadUrl is not None:
            AbbyyOnlineSdk().download_result(task, result_file_path)
            print("Result was written to {}".format(result_file_path))
        else:
            print("Error processing task")


def recognize_file(image_data, image_path):
    ct = time.time()
    logging.info('start recognize_file')
    file_name, ext = os.path.splitext(image_path)
    file_name += '_recognized'
    target_file = file_name + '.xml'
    language = 'English'
    output_format = 'xml'
    _recognize_file(image_data, target_file, language, output_format)
    duration = time.time() - ct
    logging.info('finished recognize_file %s', round(duration, 2))
    return target_file
