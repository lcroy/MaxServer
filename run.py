from flask import Flask, request, jsonify, render_template, send_file
from services.language_service.intent_recognition.max_predictor import *
import json
import os


app = Flask(__name__)
app.add_url_rule('/photos/<path:filename>', ...)
tasks = []

#update the
@app.route('/get_conv/', methods=['GET'])
def get_conv():
    filename = os.path.join(app.static_folder, 'data', 'conv.json')
    with open(filename) as json_file:
        data = json.load(json_file)

    return jsonify(data)


# calling the language service + robot service
@app.route('/get_service/', methods=['GET'])
def get_service():
    # bad requests
    if not request.args or 'message' not in request.args:
        return jsonify(
            service_name = 'none',
            intent='none',
            slot='none',
            required_slot = [],
            result= 'bad_request'
        )
    else:
        user_utterance = request.args.get('message')
        requested_service = request.args.get('requested_service')
        client_slot_result = json.loads(request.args.get('client_slot_result'))
        if len(user_utterance) > 0:

            # Predict the requested intent
            pred_result, pred_service, language_service_result_flag, updated_client_slot_result, required_slot_list = pred_intent_slot(user_utterance, client_slot_result, requested_service)

            # Search the service (robot service or other)
            # Max don't understand
            if language_service_result_flag == 0:
                return jsonify(
                    service_name=requested_service,
                    intent='none',
                    slot='none',
                    required_slot=[],
                    result='do_not_understand'
                )
            # everything is fine
            else:

                if pred_service == 'main':
                    return jsonify(
                        service_name=pred_service,
                        intent=pred_result['intent'],
                        slot=updated_client_slot_result,
                        required_slot=required_slot_list,
                        result='good_result'
                    )
                else:
                    return jsonify(
                        service_name=pred_service,
                        intent=pred_result['intent'],
                        slot=updated_client_slot_result,
                        required_slot=required_slot_list,
                        result='good_result'
                    )
        # user's utterance is empty
        else:
            return jsonify(
                service_name='none',
                intent='none',
                slot=client_slot_result,
                required_slot=[],
                result='did_not_catch'
            )

# calling the index
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# download the
@app.route('/download', methods=['GET'])
def downloadFile ():
    path = os.path.join(app.static_folder, 'data', 'service_list.json')
    return send_file(path, as_attachment=True)


# def parse_user_utterance(pred_result, confidence):
#
#     if confidence >= 3.8:
#
#         # if intent is leave
#         if pred_result['intent'] == 'GREETING':
#
#             return 'GREETING', random.choice(res.mia_response['greeting'])
#
#         if pred_result['intent'] == 'MISSIONCHECK':
#
#             return 'MISSIONCHECK', random.choice(res.mia_response['mirfree'])

        #     sys_info = mir.get_system_info()
        #     state_id = sys_info['state_id']
        #     # pause
        #     if state_id == 4:
        #         best_distance, cloest_location = mir.check_reach_des()
        #         # if MiR reach the destination
        #         if (best_distance <= 1.2) and (cloest_location == mission[0][4]) and (len(mission) > 0):
        #             # mission.append([person[0], object[0], size[0], color[0], destination[0]])
        #             botx.text_to_speech(cfg, "I am here to deliver the " + mission[0][3] + " " +
        #                                 mission[0][2] + " " + mission[0][1] + " to " + mission[0][
        #                                     4] + " and hand it over to " + mission[0][0])
        #             mission = mission[1:]
        #         else:
        #             botx.text_to_speech(cfg, random.choice(res.mia_response['mirbusy']) + mission[0][4])
        #     # ready
        #     if state_id == 3:
        #         pending_mission = mir.get_pending_mission()
        #         if pending_mission == False:
        #             botx.text_to_speech(cfg, random.choice(res.mia_response['mirfree']))
        #     # executing
        #     if state_id == 5:
        #         mir.put_state_to_pause()
        #         botx.text_to_speech(cfg, random.choice(res.mia_response['mirbusy']) + mission[0][4])
        #         # continue MiR
        #         mir.put_state_to_execute()
        #     # if result == 'None':
        #     #     botx.text_to_speech_local(random.choice(res.mia_response['mirfree']))
        #     # else:
        #     #     # pause MiR
        #     #     mir.put_state_to_pause()
        #     #     botx.text_to_speech_local(random.choice(res.mia_response['mirbusy']) + result)
        #     #     # continue MiR
        #     #     mir.put_state_to_execute()
        #     continue
        #
        # if pred_result['intent'] == 'POSITIONCHECK':
        #     # botx.text_to_speech(cfg, "I will let you know where am I when I connect with MiR.")
        #     dist, name = mir.get_nearest_position()
        #     botx.text_to_speech(
        #         cfg, random.choice(
        #             res.mia_response['location']) + name)
        #     continue
        # #
        # # if text.count('bye') > 0:
        # #     botx.text_to_speech(cfg, random.choice(res.Botx_Res['goodbye']))
        # #     break
        #
        # # if intent is checking battery information
        # if pred_result['intent'] == 'BATTERYCHECK':
        #     result = mir.get_system_info()
        #     battery_per = str(int(result['battery_percentage'])) + '%'
        #     # botx.text_to_speech(cfg, random.choice(res.mia_response['battery']) + battery_per)
        #     botx.text_to_speech(cfg, random.choice(res.mia_response['battery']) + battery_per)
        #     continue
        #
        # if pred_result['intent'] == 'ASKHELP':
        #     # get queued missions
        #     result = mir.get_exe_mission()
        #
        #     print(result)
        #     if result == 'None':
        #         # botx.text_to_speech(cfg, random.choice(res.mia_response['mirfeetohelp']))
        #         botx.text_to_speech(cfg, random.choice(res.mia_response['mirfeetohelp']))
        #
        #         while True:
        #             text = botx.speech_to_text()
        #             # intent identification
        #             pred_result, confidence = run_pred_mir(cfg, text, 1, "cuda")
        #             if confidence >= 3.8:
        #                 if pred_result['intent'] == 'DELIVERY':
        #                     obtain_order(botx, mir, cfg, pred_result)
        #                     break
        #                 else:
        #                     # botx.text_to_speech(cfg, random.choice(res.mia_response['mirnottalkinmission']))
        #                     botx.text_to_speech(cfg, random.choice(res.mia_response['mirnottalkinmission']))
        #                     break
        #     else:
        #         # pause MiR
        #         mir.put_state_to_pause()
        #         # botx.text_to_speech(cfg, random.choice(res.mia_response['mirbusybuthelp']))
        #         botx.text_to_speech(cfg, random.choice(res.mia_response['mirbusybuthelp']))
        #         # enter a loop to get new mission
        #         while True:
        #             text = botx.speech_to_text()
        #             # intent identification
        #             pred_result, confidence = run_pred_mir(cfg, text, 1, "cuda")
        #             if confidence >= 3.8:
        #                 if pred_result['intent'] == 'DELIVERY':
        #                     obtain_order(botx, mir, cfg, pred_result)
        #                     mir.put_state_to_execute()
        #                 else:
        #                     # botx.text_to_speech(cfg, random.choice(res.mia_response['mirnottalkinmission']))
        #                     botx.text_to_speech(cfg, random.choice(res.mia_response['mirnottalkinmission']))
        #                     mir.put_state_to_execute()
        #                     break
        #
        #         mir.put_state_to_execute()
        #     continue
        #
        # if pred_result['intent'] == 'STATESTOP':
        #     # botx.text_to_speech(cfg, "I believe you want me to stop")
        #     mir.put_state_to_pause()
        #     # botx.text_to_speech(cfg,
        #     #                     random.choice(
        #     #                         res.mia_response['wait']))
        #     botx.text_to_speech(
        #         cfg, random.choice(
        #             res.mia_response['wait']))
        #     continue
        #
        # if pred_result['intent'] == 'STATERUN':
        #     # botx.text_to_speech(cfg, "So, I am good to go")
        #     mir.put_state_to_execute()
        #     # botx.text_to_speech(cfg,
        #     #                     random.choice(
        #     #                         res.mia_response['continue']))
        #     botx.text_to_speech(
        #         cfg, random.choice(
        #             res.mia_response['continue']))
        #     continue
        #
        # # if pred_result['intent'] == 'DELIVERY':
        # #     r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\n。！，]+'
        # #     botx.text_to_speech(cfg, "I believe you want me to deliver things")
        # #     for item in pred_result['slot']:
        # #         if item[1] == 'B-DELIVERY_PERSON':
        # #             if (re.sub(r,'',item[0]) != 'max'):
        # #                 botx.text_to_speech(cfg, "The person who should receive this is " + re.sub(r,'',item[0]))
        # #         if item[1] == 'B-DELIVERY_OBJECT':
        # #             if (re.sub(r, '', item[0]) != 'it'):
        # #                 botx.text_to_speech(cfg, "The object is " + re.sub(r, '', item[0]))
        # #         if item[1] == 'B-DELIVERY_POSITION':
        # #             botx.text_to_speech(cfg, "The destination is " + re.sub(r, '', item[0]))
        # #         if item[1] == 'B-DELIVERY_OBJECT_COLOR':
        # #             botx.text_to_speech(cfg, "The object color is " + re.sub(r, '', item[0]))
    #     # #         if item[1] == 'B-DELIVERY_OBJECT_SIZE':
    #     # #             botx.text_to_speech(cfg, "The object size is " + re.sub(r, '', item[0]))
    #     # #     continue
    # else:
    #     return 'None', 'What you said is beyond my understanding or not belong to any skill I have.'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
