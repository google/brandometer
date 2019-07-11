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

var controller = new Controller(fullConfiguration.ui_config, fullConfiguration.survey_config);

function runFSM() {
    switch (controller.creativeState) {
        case "BEGIN":
            controller.init();
            controller.renderHTML();
            controller.creativeState = "RENDERED_HTML";
        case "RENDERED_HTML":
            //render carousel if there
            if (controller.isCarousel()) {
                controller.renderCarousel();
                controller.creativeState = "RENDERED_CAROUSEL";
                break;
            }

        case "RENDERED_QUESTION":
            controller.creativeState = "RENDERED_QUESTION";
            if (controller.renderNextQuestion()) {
                break;
            }

        case "THANK_YOU":
            controller.fireTrackingPixel();
            controller.sendCollectedResponseToServer();
            controller.creativeState = "THANK_YOU";
            controller.renderThankyou();
            break;
    }
}