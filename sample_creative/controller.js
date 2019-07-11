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

function Controller(uiConfig, surveyConfig) {
  return {
    uiConfig: uiConfig,
    surveyConfig: surveyConfig,
    renderedQuestionId: -1,
    uiElementObjects: {},
    collectedResponses: {},
    creativeState: 'BEGIN',
    questionMap: {},
    time_measurement:
      { start_time: null, q1_start_time: null, question_end_time: null },
    visualOptions: {},

    init: function () {
      for (var questionIndex = 0;
        questionIndex < this.surveyConfig.questions.length;
        questionIndex++) {
        this.collectedResponses[String(
          this.surveyConfig.questions[questionIndex].id)] = [];

        this.visualOptions[String(
          this.surveyConfig.questions[questionIndex].id)] = [];


        // Setup question map
        this.questionMap[String(
          this.surveyConfig.questions[questionIndex].id)] =
          this.surveyConfig.questions[questionIndex];
      }

      // Update Next Button Text from configuration

      document
        .getElementById(
          this.uiConfig.component_selectors.next_button.container)
        .innerText = this.uiConfig.component_selectors.next_button.text;

      // set the clickTag to based on configured exit
      clickTag = this.surveyConfig.exit_url;

      // Measure render time
      this.time_measurement.start_time = new Date();

      //Fire Global Tag Config
      this.setupGlobalTags();
    },

    // Check cookie to get User ID or Drop a new one
    getOrGenerateCookieId: function () {
      var cookieIdRegexMatch = /bomu=([^;]+)/.exec(document.cookie);
      return (cookieIdRegexMatch == null) ? this.setCookieId() :
        cookieIdRegexMatch[1];
    },

    setCookieId: function () {
      var cookieId = this.uuidv4();
      document.cookie = 'bomu=' + cookieId + '; path=/; domain=.mdn.net;';
      return cookieId;
    },

    uuidv4: function () {
      var uuid = null;
      try {
        uuid = ([1e7] + -1e3 + -4e3 + -8e3 + -1e11)
          .replace(
            /[018]/g,
            function (c) {
              return (c ^
                crypto.getRandomValues(new Uint8Array(1))[0] &
                15 >> c / 4)
                .toString(16);
            });
      } catch (e) {
        uuid = 'xxxxxxxx-xxxx-0xxx-yxxx-xxxxxxxxxxxx'.replace(
          /[xy]/g, function (c) {
            var r = Math.random() * 16 | 0,
              v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
          });
      }

      return uuid;
    },

    setupEventHandlers: function () {
      // Set Next Button Event Handlers
      document
        .getElementById(
          this.uiConfig.component_selectors.next_button.container)
        .addEventListener('click', runFSM);


      // Set Option Selection Event Handlers
      var surveyOptionsUIConfig =
        this.uiConfig.component_selectors.survey.options;
      for (var optIndex = 0; optIndex < surveyOptionsUIConfig.max_options;
        optIndex++) {
        document
          .getElementById(
            surveyOptionsUIConfig.option_prefix.container + optIndex)
          .addEventListener('click', this.handleOptionSelection.bind(this));
      }
    },

    isCarousel: function () {
      return (this.surveyConfig.carousel_images.length > 0);
    },

    renderCarousel: function () {
      // make carousel visible
      document.getElementById('carousel_container').removeAttribute('class');

      // Hide all other containers
      document
        .getElementById(this.uiConfig.component_selectors.survey.container)
        .setAttribute('class', 'invisible');

      document
        .getElementById(this.uiConfig.component_selectors.thankyou.container)
        .setAttribute('class', 'invisible');

      // console.log(this.surveyConfig.thankyou_text);
      document
        .getElementById(
          this.uiConfig.component_selectors.next_button.container)
        .style.visibility = 'hidden';
      document
        .getElementById(this.uiConfig.component_selectors.comment.container)
        .style.visibility = 'hidden';

      // Render Carousel components
    },

    nextCarouselSlide: function () {

    },

    previousCarouselSlide: function () {

    },

    recordQuestionResponse: function () {
      if (this.renderedQuestionId < 0) return true;

      for (var optionIndex = 0; optionIndex <
        this.uiConfig.component_selectors.survey.options.max_options;
        optionIndex++) {
        var optionContainer = document.getElementById(
          this.uiConfig.component_selectors.survey.options.option_prefix
            .container +
          optionIndex);

        if (optionContainer.getAttribute('selected') == 'true') {
          this
            .collectedResponses[String(
              this.questionMap[this.renderedQuestionId].id)]
            .push(optionContainer.getAttribute('oid'));

          this.visualOptions[String(
            this.questionMap[this.renderedQuestionId].id)]
            .push(String.fromCharCode(65 + optionIndex));
        }

        optionContainer.removeAttribute('selected');
      }

      // Record time of 1st response
      if (this.renderedQuestionId == 1) {
        this.time_measurement.q1_start_time = new Date();
      }

      return this.collectedResponses[this.renderedQuestionId].length > 0;
      // console.log(this.collectedResponses);
    },

    renderNextQuestion: function () {

      if (!this.recordQuestionResponse()) return true;

      // Increment renderedId to get the next Question Id
      // this.renderedQuestionId++;
      // lookup next question based on decision_tree
      // get response
      if (this.renderedQuestionId == -1) {
        this.renderedQuestionId = this.surveyConfig.questions[0].id;
      } else {
        this.renderedQuestionId =
          this.questionMap[this.renderedQuestionId]
            .next_question[this.collectedResponses[this.renderedQuestionId]
          [0]];
      }


      // Return if all questions rendered OR decision tree based end
      if (this.renderedQuestionId > this.surveyConfig.questions.length ||
        this.renderedQuestionId == 'end') {
        // Record time of last response
        this.time_measurement.question_end_time = new Date();
        return false;
      }

      var question = this.questionMap[this.renderedQuestionId];

      this.renderQuestion(question);

      // shuffle array only if not ORDERED type question
      if (question.type != 'ORDERED') {
        this.shuffleArray(question.options);
      }

      this.renderOptions(question.options);


      // hide Next Button
      document
        .getElementById(
          this.uiConfig.component_selectors.next_button.container)
        .style.visibility =
        (this.isCurrentQuestionSingleOption()) ? 'hidden' : 'visible';

      // show comment section if multiple options
      document
        .getElementById(this.uiConfig.component_selectors.comment.container)
        .innerHTML = (this.isCurrentQuestionSingleOption()) ?
          '' :
          this.uiConfig.component_selectors.comment.text;
      return true;
    },

    renderQuestion: function (question) {
      // Persist Rendered QuestionId as an element Attribute
      document
        .getElementById(
          this.uiConfig.component_selectors.survey.question.container)
        .setAttribute('qid', question.id);

      // set QuestionText
      document
        .getElementById(
          this.uiConfig.component_selectors.survey.question.text)
        .innerHTML = question.text;
    },

    renderOptions: function (questionOptions) {
      // create a local referenc to uiConfig
      var optionsUIConfig =
        this.uiConfig.component_selectors.survey.options.option_prefix;

      var maxOptions =
        this.uiConfig.component_selectors.survey.options.max_options;

      for (var optIndex = 0; optIndex < maxOptions; optIndex++) {
        var optionContainer =
          document.getElementById(optionsUIConfig.container + optIndex);

        // remove the visibility_controlling class
        /*var optionContainerClasses = optionContainer.className
         .replace(/invisible/g, "")
         .replace(/\s{2,}|^\s+|\s+$/g, " ");
         */
        if (optIndex < questionOptions.length) {
          // Make the option container visible
          optionContainer.style.visibility = 'visible';

          // Set OID on the option container
          optionContainer.setAttribute('oid', questionOptions[optIndex].id);
          optionContainer.setAttribute('role', questionOptions[optIndex].role);
          // Set Option Label (A-D)
          // document.getElementById(optionsUIConfig.label + optIndex).innerHTML
          // =
          //    String.fromCharCode(65 + optIndex);

          // Set option text
          document.getElementById(optionsUIConfig.text + optIndex).innerHTML =
            questionOptions[optIndex].text;
        } else {
          // hide unused option-divs
          // optionContainerClasses += " invisible";
          optionContainer.style.visibility = 'hidden';
        }
        // optionContainer.className = optionContainerClasses;
      }
    },

    handleOptionSelection: function (event) {
      var optionContainer = event.target.parentElement;

      // Toggle Selected Attribute
      if (optionContainer.getAttribute('selected') == null) {
        optionContainer.setAttribute('selected', 'true');
      } else {
        optionContainer.removeAttribute('selected');
      }

      if (optionContainer.getAttribute('role') == 'reset') {
        this.resetOptions();
      }

      if (this.isCurrentQuestionSingleOption()) {
        this.moveToNextQuestion();
      }
    },

    moveToNextQuestion: function () {
      // simulate Next Button Click
      document
        .getElementById(
          this.uiConfig.component_selectors.next_button.container)
        .click();
    },

    resetOptions: function () {
      var options = document.getElementsByClassName('Abox');

      for (i = 0; i < options.length; i++) {
        options[i].setAttribute('selected', false);
        event.target.parentElement.setAttribute('selected', 'true');
      }
      this.moveToNextQuestion();
    },

    isCurrentQuestionSingleOption: function () {
      if (this.questionMap[this.renderedQuestionId] != undefined) {

        var question = this.questionMap[this.renderedQuestionId];
        return (question.type == 'SINGLE_OPTION' || question.type == 'ORDERED');
      }
    },

    renderHTML: function () {
      this.setupEventHandlers();
      // console.log(controller.uiConfig.background_color);
      document.getElementById('master_container').style['background-color'] =
        this.uiConfig.background_color;
    },

    renderThankyou: function () {
      // document.getElementById("carousel_container").setAttribute("class",
      // "invisible");

      document
        .getElementById(this.uiConfig.component_selectors.survey.container)
        .setAttribute('class', 'invisible');

      document
        .getElementById(this.uiConfig.component_selectors.thankyou.container)
        .setAttribute('class', 'thankyoucontainer');

      document.getElementById(this.uiConfig.component_selectors.thankyou.text)
        .innerHTML = this.surveyConfig.thankyou_text;


      // console.log(this.surveyConfig.thankyou_text);
      document
        .getElementById(
          this.uiConfig.component_selectors.next_button.container)
        .style.visibility = 'hidden';
      document
        .getElementById(this.uiConfig.component_selectors.comment.container)
        .style.visibility = 'hidden';

      // check if google form exit
      if (this.surveyConfig['google_form_exit'] &&
        this.surveyConfig['google_form_exit'] != '') {
        window.open(this.surveyConfig.google_form_exit.replace(
          /\{responses\}/g,
          encodeURIComponent(
            this.getEncodedResponseString(this.collectedResponses)) +
          '**' + encodeURIComponent(surveyConfig.id) + '**' +
          encodeURIComponent(surveyConfig.seg) + '**'));
      }
    },

    shuffleArray: function (array) {
      var currentIndex = array.length - 1, temporaryValue, randomIndex;
      // While there remain elements to shuffle...
      while (0 !== currentIndex) {
        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        // console.log("randomIndex: " + randomIndex, "currentIndex: " +
        // currentIndex);
        currentIndex -= 1;
        // And swap it with the current element.
        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
      }
      return array;
    },

    fireTrackingPixel: function () {
      this.surveyConfig.trackers.forEach(function (pixelUrl) {
        this.insertPixel(pixelUrl);
      }.bind(this));

      this.fireGlobalTagsEvents();
    },


    setupGlobalTags: function () {
      if (this.surveyConfig.global_tags != null &&
        this.surveyConfig.global_tags.length > 0) {
        // Insert master tag
        this.insertScript(
          null, 'https://www.googletagmanager.com/gtag/js?id=AW-968433116',
          'head');

        this.insertScript(
          'window.dataLayer = window.dataLayer || [];\n' +
          'function gtag(){dataLayer.push(arguments);}\n' +
          'gtag(\'js\', new Date());',
          null, 'head');

        // insert child global tag setup
        this.insertScript(this.surveyConfig.global_tags
          .map(function (gTag) {
            return 'gtag(\'config\', \'' +
              gTag.property_id + '\');';
          })
          .join('\n'));
      }
    },

    fireGlobalTagsEvents: function () {
      if (this.surveyConfig.global_tags != null &&
        this.surveyConfig.global_tags.length > 0) {
        this.insertScript(this.surveyConfig.global_tags
          .map(function (gTag) {
            return 'gtag(' + gTag.event_details + ');';
          })
          .join('\n'));
      }
    },

    sendCollectedResponseToServer: function () {
      this.insertPixel(this.surveyConfig.response_server);
    },

    insertScript: function (scriptString, srcString, position) {
      var scriptTag = document.createElement('script');
      if (srcString == null) {
        scriptTag.innerHTML = scriptString;
      } else {
        scriptTag.setAttribute('src', srcString);
      }

      if (position == null || position == 'body') {
        document.body.appendChild(scriptTag);
      } else {
        document.head.appendChild(scriptTag);
      }
    },

    insertPixel: function (url) {
      var macroFilledUrl = this.fillMacrosInUrl(url);

      var pixelFrame = document.createElement('iframe');
      pixelFrame.setAttribute('width', '0');
      pixelFrame.setAttribute('height', '0');
      pixelFrame.setAttribute('src', macroFilledUrl);
      document.body.appendChild(pixelFrame);

      // console.log("fired: " + macroFilledUrl);
    },


    getEncodedResponseString: function (responses) {
      return encodeURIComponent(Object.keys(responses)
        .map(function (x) {
          return String(x) + ':' +
            responses[x].join('');
        }.bind(this))
        .join('|'));
    },

    fillMacrosInUrl: function (url) {
      return url
        .replace(
          /\{bomid\}/g, encodeURIComponent(this.getOrGenerateCookieId()))
        .replace(/\{survey_id\}/g, encodeURIComponent(surveyConfig.id))
        .replace(
          /\{responses\}/g,
          this.getEncodedResponseString(this.collectedResponses))
        .replace(
          /\{visual_responses\}/g,
          this.getEncodedResponseString(this.visualOptions))
        .replace(/\{seg\}/g, encodeURIComponent(surveyConfig.seg))
        .replace(/\{time_measurement\}/g, this.measureSurveyTimes())
        .replace(
          /\{size\}/g,
          encodeURIComponent(
            String(uiConfig.creative_size.width) + 'x' +
            String(uiConfig.creative_size.height)))
        .replace(
          /\{random_timestamp\}/g,
          encodeURIComponent(this.getRandomTimestamp()));
    },

    getRandomTimestamp: function () {
      return String(10000000 * Math.random());
    },

    measureSurveyTimes: function () {
      return '' +
        (this.time_measurement.q1_start_time -
          this.time_measurement.start_time) +
        '|' +
        (this.time_measurement.question_end_time -
          this.time_measurement.q1_start_time);
    },


  };
}
