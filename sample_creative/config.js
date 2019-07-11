/*
Copyright 2019 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

var fullConfiguration = {
  "survey_config": {
    // TODO: Set receiver domain to match your host.
    "response_server": "https://[your_target url]/measure?type=survey&id={survey_id}&seg={seg}&response={responses}&visual={visual_responses}&creative_size={size}&randomtimestamp={random_timestamp}&bomid={bomid}&times={time_measurement}",
    // TODO: Set a unique ID for each survey
    "id": "[your_unique_id]",
    // TODO: Create new creatives for each segment (e.g. demographics) of interest
    "seg": "default",
    // TODO: Update questions and options for each survey
    "questions": [
      {
        "id": "1",
        "type": "SINGLE_OPTION",
        "text": "Test question 1",
        "options": [
          {
            "id": "A",
            "role": "option",
            "text": "AA"
          },
          {
            "id": "B",
            "role": "option",
            "text": "BB"
          },
          {
            "id": "C",
            "role": "option",
            "text": "CC"
          },
          {
            "id": "D",
            "role": "option",
            "text": "DD"
          },
          {
            "id": "E",
            "role": "option",
            "text": "EE"
          }
        ],
        "next_question": {
          "A": "2",
          "B": "2",
          "C": "2",
          "D": "2",
          "E": "2"
        }
      },
      {
        "id": "2",
        "type": "SINGLE_OPTION",
        "text": "Test question 2",
        "options": [
          {
            "id": "F",
            "role": "option",
            "text": "FF"
          },
          {
            "id": "G",
            "role": "option",
            "text": "GG"
          },
          {
            "id": "H",
            "role": "option",
            "text": "HH"
          }
        ],
        "next_question": {
          "F": "end",
          "G": "end",
          "H": "end"
        }
      }
    ],
    "exit_url": "https://www.google.com",
    "carousel_images": [],
    "thankyou_text": "Thank You",
    "trackers": [
      ""
    ]
  },
  "ui_config": {
    "creative_size": {
      "width": 300,
      "height": 250
    },
    "background_color": "#008000",
    "carousel_config": {},
    "component_selectors": {
      "next_button": {
        "container": "next_button",
        "text": "Next"
      },
      "thankyou": {
        "container": "thankyou_container",
        "text": "thankyou_text"
      },
      "survey": {
        "container": "survey_container",
        "question": {
          "text": "question_text",
          "container": "question_container"
        },
        "options": {
          "max_options": 5,
          "option_prefix": {
            "text": "option_text_",
            "container": "option_container_",
            "label": "option_label_"
          }
        }
      },
      "comment": {
        "container": "question_comment",
        "text": "Choose all applicable"
      }
    }
  }
};