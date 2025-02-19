# K3s Cluster Setup

## Содержание:
- [Описание](#описание)
- [Основные этапы работы с кластером](#основные-этапы-работы-с-кластером)
- [Работа с кластером k3d](#работа-с-кластером-k3d)
  - [Поднятие кластера k3d](#поднятие-кластера-k3d)
  - [Настройка кластера k3d](#настройка-кластера-k3d)
- [Deploy helm charts](#deploy-helm-charts)
- [Установка мониторинга](#установка-мониторинга)
- [Настройка DNS на localhost](#настройка-dns-на-localhost)

---

## Описание
Этот репозиторий содержит базовую структуру кластера K3s, включая описание папок, файлов и основных этапов развертывания.
Здесь представлены два варианта развертывания:
- **Локально с использованием k3d** – подходит для тестирования и локальной разработки.

### Структура папок

```plaintext
./k3s/               # Конфигурационные файлы K3s
  ./manifests/         # Манифесты для развертывания ресурсов
  ./network-policy/    # Файлы политики безопасности сети
  ./helm/              # Helm-чарты для деплоя сервисов
```

---

## Основные этапы работы с кластером

1. **Поднимаем кластер:**
   - Описываем YAML-файл конфигурации.
   - Определяем необходимые ресурсы.
   - Запускаем кластер.
2. **Применяем манифесты:**
   - Создаем namespace.
   - Разворачиваем ingress-контроллеры.
   - Опционально настраиваем storage-class.
3. **Настраиваем Network Policy:**
   - Описываем политики безопасности для ingress и других namespaces.
4. **Деплоим чарты в namespaces:**
   - Загружаем необходимые секреты.
   - Разворачиваем приложение.

---

## Работа с кластером k3d

### Поднятие кластера k3d

Конфигурация кластера описана в `k3d-cluster.yaml`.

- **Создание кластера:**
  ```sh
  k3d cluster create --config k3d-cluster.yaml
  ```
- **Проверка состояния:**
  ```sh
  k3d cluster list
  ```
- **Удаление кластера:**
  ```sh
  k3d cluster delete <название-кластера>
  ```

Настройка контекста для kubectl:
```sh
kubectl config get-contexts
k3d kubeconfig get <название-кластера> > ~/.kube/config
kubectl config use-context <имя-контекста>
kubectl cluster-info
```

---

### Настройка кластера k3d

- **Применение манифестов:**
  ```sh
  kubectl apply -f ./manifests/namespaces.yaml
  kubectl apply -f ./manifests/storage-class.yaml
  ```
- **Развертывание ingress-nginx:**
  ```sh
  helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
  helm repo update
  helm install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx
  ```
- **Применение политик безопасности:**
  ```sh
  kubectl apply -f ./network-policy/cache-policy.yaml
  kubectl apply -f ./network-policy/database-policy.yaml
  kubectl apply -f ./network-policy/ingress-policy.yaml
  ```
- **Удаление политики безопасности:**
  ```sh
  kubectl delete networkpolicy --all -n <namespace>
  ```

---

## Deploy helm charts

Перед деплоем приложения необходимо загрузить его Docker-образ в кластер:
```sh
k3d image import <имя-образа> --cluster <название-кластера>
```

Развертывание сервисов:
```sh
helm install database ./helm/postgresql -n database
helm install cache ./helm/redis -n cache
helm install app ./helm/app -n app
```

Просмотр секретов и логов:
```sh
kubectl get secrets -n <namespace>
kubectl logs <pod-name> -n <namespace>
```

Обновление чартов:
```sh
helm upgrade app ./helm/app -n app --debug
```

---

## Установка мониторинга

Установка Prometheus и Grafana:
```sh
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install monitoring-stack prometheus-community/kube-prometheus-stack --namespace monitoring
kubectl apply -f ./helm/grafana/ingress-grafana.yaml
```

---

## Настройка DNS на localhost

Добавьте следующие строки в `/etc/hosts` для доступа к сервисам:
```plaintext
127.0.0.1 web.local
127.0.0.1 grafana.local
```

Теперь можно зайти на веб-интерфейсы сервисов через браузер.



