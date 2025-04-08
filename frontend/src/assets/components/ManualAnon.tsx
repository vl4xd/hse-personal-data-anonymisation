// import React from 'react';
import {useCallback, useEffect, useState} from 'react'
import { Input, Select, SelectProps, Button, Typography } from 'antd';

import axios from 'axios';

const { TextArea } = Input;
const { Title } = Typography;

function ManualAnon() {

    const [optionsModels, setOptionsModels] = useState<SelectProps['options']>([]);
    const [defaultModelValue, setDefaultModelValue] = useState<string>('')
    const [isModelsLoading, setIsModelsLoading] = useState(false);
    const fetchModels = () => {

        setIsModelsLoading(true) // устанавливаем значение загрузки models

        axios.get('http://127.0.0.1:8000/models').then(r => {
            const modelsResponse = r.data;
            const newOptions = [];

            for (const key in modelsResponse) {
                newOptions.push({
                    value: key as string,
                    label: modelsResponse[key] as string
                });
            }

            setOptionsModels(newOptions);
            if (newOptions.length > 0) {
                setDefaultModelValue(newOptions[0].value)
            }
        })
        .catch(() => {
            console.error('Ошибка при выполнении запроса моделей.');
        })
        .finally(() => {
            setIsModelsLoading(false) // устанавливаем значение загрузки models
        });
    }


    const [optionsLabels, setOptionsLabels] = useState<SelectProps['options']>([]);
    const [defaultLabel, setDefaultLabels] = useState<string[]>([]);
    const [isLabelsLoading, setIsLabelsLoading] = useState(false);
    const fetchLabels = useCallback((modelIndex: string) => {
        const modelIndexNumber = parseInt(modelIndex)
        if (isNaN(modelIndexNumber)) return;

        setIsLabelsLoading(true) // устанавливаем значение загрузки labels

        axios.post('http://127.0.0.1:8000/labels', {'model_index': parseInt(modelIndex)}).then(r => {
            const labels = Object.entries(r.data).map(([key, value]) => ({
                value: key as string,
                label: value as string
              }));
            setOptionsLabels(labels);
            setDefaultLabels([]);
        })
        .catch(() => {
            console.error('Ошибка при выполнении запроса лейблов.');
        })
        .finally(() => {
            setIsLabelsLoading(false) // устанавливаем значение загрузки labels
        });
    }, []);


    const [optionsAnonymizers, setOptionsAnonymizers] = useState<Array<{
        value: string;
        label: string;
        need_mask: boolean;
    }>>([]);
    const [needMask, setNeedMask] = useState(false);
    const [defaultAnonymizerValue, setDefaultAnonymizerValue] = useState<string>('');
    const [isAnonymizersLoading, setIsAnonymizersLoading] = useState(false);
    const fetchAnonymizers = useCallback(() => {

        setIsAnonymizersLoading(true) // устанавливаем значение загрузки anonymizers

        axios.get<{ [key: string]: { name: string; need_mask: boolean } }>('http://127.0.0.1:8000/anonymizers').then(r => {
            const anonymizers = Object.entries(r.data).map(
                ([key, value]: [string, { name: string; need_mask: boolean }]) => ({
                
                value: key as string,
                label: value.name,
                need_mask: value.need_mask

              }));
            
            setOptionsAnonymizers(anonymizers);
            
            if (anonymizers.length > 0) {
                setDefaultAnonymizerValue(anonymizers[0].value)
                setNeedMask(anonymizers[0].need_mask);
            }
        })
        .catch(() => {
            console.error('Ошибка при выполнении запроса анонимизаторов.');
        })
        .finally(() => {
            setIsAnonymizersLoading(false) // устанавливаем значение загрузки anonymizers
        });
    }, []);

    // изменение значения need_mask для отображения дополнительного поля ввода маски
    const handleAnonymizerChange = (value: string) => {
        const selected = optionsAnonymizers.find(a => a.value === value);
        if (selected) {
            setDefaultAnonymizerValue(value);
            setNeedMask(selected.need_mask);
        }
    };


    // Получение данных models при загрузке страницы
    useEffect(() => {
        fetchModels()
    }, []);

    // Получение данных anonymizers при загрузке страницы
    useEffect(() => {
        fetchAnonymizers()
    }, []);

    // Получение данных labels при загрузке страницы
    useEffect(() => {
        if (defaultModelValue) {
            fetchLabels(defaultModelValue);
        }
    }, [defaultModelValue, fetchLabels]);

    // Обработчик изменения модели и получение для нее labels
    const handleModelChange = (value: string) => {
        // Обновляем только если значение изменилось
        if (value !== defaultModelValue){
            setDefaultModelValue(value)
        }
    };

    const [text, setText] = useState('');
    const [mask, setMask] = useState('');
    const [result, setResult] = useState<{
      text: string;
      entities: Array<{
        label: string;
        text: string;
        start_char: number;
        end_char: number;
      }>;
    } | null>(null);
    const [isPredictionLoading, setIsPredictionLoading] = useState(false);
    const predictData = () => {
        setIsPredictionLoading(true);

        const requestData = {
            anonymizer_index: parseInt(defaultAnonymizerValue),
            anon_mask: needMask ? mask : "",
            model_index: parseInt(defaultModelValue),
            labels_index: defaultLabel.map(value => parseInt(value)),
            text: text,
        };

        axios.post('http://127.0.0.1:8000/predict', requestData)
            .then(r => {
                setResult(r.data)
            })
            .catch(() => {
                console.error('Ошибка при выполнении запроса анонимизации текста.');
            })
            .finally(() => {
                setIsPredictionLoading(false);
            });
    };

    return (
        <>
            <div style={{marginTop: 10, marginBottom: 10}}>
                <Title level={5}>
                    1. Выбирите модель (разные классы сущностей)
                </Title>
                <Select
                    size={'middle'}
                    value={defaultModelValue || undefined}
                    onChange={handleModelChange}
                    style={{ width: '100%' }}
                    options={optionsModels}
                    loading={isModelsLoading}
                />
            </div>

            <div style={{marginTop: 10, marginBottom: 10}}>
                <Title level={5}>
                    2. Выбирите класс(ы) сущностей, которые будут найдены в тексте (пустой выбор = все классы)
                </Title>
                <Select
                    mode="multiple"
                    value={defaultLabel}
                    onChange={setDefaultLabels}
                    style={{ width: '100%' }}
                    placeholder="Выберите классы сущностей"
                    options={optionsLabels}
                    loading={isLabelsLoading}
                />
            </div>

            <div style={{marginTop: 10, marginBottom: 10}}>
                <Title level={5}>
                    3. Выбирите тип анонимизации
                </Title>
                <Select
                    size={'middle'}
                    value={defaultAnonymizerValue || undefined}
                    onChange={handleAnonymizerChange}
                    style={{ width: '100%' }}
                    options={optionsAnonymizers}
                    loading={isAnonymizersLoading}
                />                
            </div>

            <div style={{marginTop: 10, marginBottom: 10}}>
                {
                        
                        needMask && <Title level={5}>4. Задайте маску</Title>
                }
                {
                    needMask && <Input 
                                    showCount
                                    maxLength={30}
                                    value={mask}
                                    onChange={(e) => setMask(e.target.value)}
                                    placeholder="Введите маску анонимизации"
                                />
                }
            </div>

            <div style={{marginTop: 10, marginBottom: 10}}>
                <Title level={5}>5. Введите текст</Title>

                <TextArea 
                placeholder="Введите текст"
                autoSize
                value={text}
                onChange={(e) => setText(e.target.value)}/>
            </div>

            <div style={{marginTop: 10, marginBottom: 10}}>
                <Button
                    type="primary"
                    loading={isPredictionLoading}
                    onClick={predictData}
                    iconPosition="end"
                >
                Анонимизировать
                </Button>
            </div>

            {result && (
                    <div style={{ marginTop: 20 }}>
                        <h3>Результат анонимизации:</h3>
                        <p style={{ whiteSpace: "pre-wrap" }}>{result.text}</p>
                        <br></br>
                        <h4>Найденные сущности:</h4>
                        <ul>
                        {result.entities.map((entity, index) => (
                            <li key={index}>
                            {entity.label}: {entity.text} (позиции {entity.start_char}-{entity.end_char})
                            </li>
                        ))}
                        </ul>
                    </div>
                )}
        </>
    );
};

export default ManualAnon;