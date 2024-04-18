import os
import cv2
import time
import argparse

import torch
import model.detector
import utils.utils

if __name__ == '__main__':
    # Especifica o arquivo de configuração de treinamento
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='', 
                        help='Especifique o arquivo de perfil de treinamento *.data')
    parser.add_argument('--weights', type=str, default='', 
                        help='O caminho do modelo .pth a ser transformado')
    opt = parser.parse_args()
    
    cfg = utils.utils.load_datafile(opt.data)
    assert os.path.exists(opt.weights), "Por favor, especifique o caminho correto do modelo"

    # Carrega o modelo
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.detector.Detector(cfg["classes"], cfg["anchor_num"], True).to(device)
    model.load_state_dict(torch.load(opt.weights, map_location=device))

    # Define o modelo em modo de avaliação
    model.eval()

    # Carrega os nomes das classes
    LABEL_NAMES = []
    with open(cfg["names"], 'r') as f:
        for line in f.readlines():
            LABEL_NAMES.append(line.strip())

    # Captura de vídeo da webcam
    cap = cv2.VideoCapture(0)

    start_time = time.time()
    frame_counter = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Pré-processamento do frame
        res_img = cv2.resize(frame, (cfg["width"], cfg["height"]), interpolation=cv2.INTER_LINEAR)
        img = res_img.reshape(1, cfg["height"], cfg["width"], 3)
        img = torch.from_numpy(img.transpose(0, 3, 1, 2))
        img = img.to(device).float() / 255.0

        # Inferência do modelo
        start = time.perf_counter()
        preds = model(img)
        end = time.perf_counter()
        inference_time = (end - start) * 1000.  # Em milissegundos
        print("Tempo de inferência: %.2fms" % inference_time)

        # Pós-processamento das previsões
        output = utils.utils.handel_preds(preds, cfg, device)
        output_boxes = utils.utils.non_max_suppression(output, conf_thres=0.3, iou_thres=0.4)

        h, w, _ = frame.shape
        scale_h, scale_w = h / cfg["height"], w / cfg["width"]

        # Desenha as caixas delimitadoras das previsões
        for box in output_boxes[0]:
            box = box.tolist()
            obj_score = box[4]
            category = LABEL_NAMES[int(box[5])]

            x1, y1 = int(box[0] * scale_w), int(box[1] * scale_h)
            x2, y2 = int(box[2] * scale_w), int(box[3] * scale_h)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
            cv2.putText(frame, '%.2f' % obj_score, (x1, y1 - 5), 0, 0.7, (0, 255, 0), 2)	
            cv2.putText(frame, category, (x1, y1 - 25), 0, 0.7, (0, 255, 0), 2)

        # Calcular e exibir FPS
        frame_counter += 1
        if frame_counter >= 10:  # Calcule FPS a cada 10 frames
            end_time = time.time()
            fps = frame_counter / (end_time - start_time)
            cv2.putText(frame, 'FPS: {:.2f}'.format(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            start_time = time.time()
            frame_counter = 0

        # Mostra o resultado
        cv2.imshow("Webcam", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera a captura da webcam e fecha todas as janelas
    cap.release()
    cv2.destroyAllWindows()
