
# Featback 🚀

**Feature-Based Reddit Product Analysis Tool**

Featback is a tool designed to help product management teams efficiently gather detailed analysis and granular feedback about specific features of their products. Unlike regular sentiment analysis, which often provides only a general sentiment score, Featback dives deeper to understand the *drivers* behind user emotions. Some features may be praised while others draw criticism, and Featback helps uncover these nuances.

For example: *What do people think about the iPhone 16? What features are most commonly reviewed? What exactly about the design do they not like — colors or weight? If they love the camera, is it about the photo quality or a zoom feature?*

Featback answers these questions by breaking down Reddit posts into **structured, feature-level insights**.

---

## 🔎 Example Breakdown

**Reddit Post**

> **Title:** “Mixed feelings about my new iPhone 16”
>
> **Text:**
> “I just got the iPhone 16 and honestly I’m disappointed. The **battery barely lasts a day** and the **screen isn’t bright enough outside**. On the positive side, the **camera takes amazing photos** and the **design looks really sleek**. But I noticed some **lag when switching between apps**, which is frustrating. By the way, does anyone know if it **supports dual SIM properly in the US**?”

---

### Reviews Table (saved as `reviews`)

| id | text                               | category    | feature           | emotion        | reason             | created\_utc |
| -- | ---------------------------------- | ----------- | ----------------- | -------------- | ------------------ | ------------ |
| …  | battery barely lasts a day         | Battery     | Battery duration  | Disappointment | Below Expectations | …            |
| …  | screen isn’t bright enough outside | Display     | Brightness levels | Disappointment | Below Expectations | …            |
| …  | camera takes amazing photos        | Camera      | Photo quality     | Excitement     | Above Expectations | …            |
| …  | design looks really sleek          | Design      | General           | Satisfaction   | Design             | …            |
| …  | lag when switching between apps    | Performance | Multitasking      | Frustration    | Reliability        | …            |

---

### Questions Table (saved as `questions`)

| id | text                                  | category     | feature          | reason          | created\_utc |
| -- | ------------------------------------- | ------------ | ---------------- | --------------- | ------------ |
| …  | supports dual SIM properly in the US? | Connectivity | Dual SIM support | Feature inquiry | …            |

---

👉 A **single Reddit post** becomes **two structured datasets** (reviews + questions), stored separately in S3 and Redshift for querying and visualization.

---

## 🛠️ Pipeline Diagram

![Pipeline Diagram](./Architecture/featback.jpg)

---

## 🧰 Key Technologies

* **AWS Services**

  * **S3** → stores raw Reddit JSON and processed feedback (Parquet).
  * **Redshift** → warehouse for efficient querying.
  * **QuickSight** → dashboards for feature-level sentiment insights.

* **OpenAI API**

  * `gpt-4o-mini` model with prompt engineering + JSON schema enforcement.

* **Docker / Docker Compose**

  * Local demo stack (MinIO + Postgres) or full cloud mode (AWS).

* **Airflow (optional)**

  * For batch orchestration of weekly runs.

* **Python Libraries**

  * `pandas`, `pyarrow`, `boto3`, `redshift_connector`, `praw`, `pandera`, `openai`.

* **Terraform (Infrastructure as Code)**

  * Defines S3 bucket, IAM role for Redshift COPY, and other infra components.

* **CI/CD with GitHub Actions**

  * Linting, unit tests, integration tests with mocked AWS/OpenAI.
  * Terraform workflows run `init`, `validate`, and `plan`.
  * Safe for public repos (no secrets required).

---

## 📂 Project Structure

```text
featback/
├─ src/featback/
│  ├─ config.py            # Centralized config
│  ├─ reddit/ingestion.py  # Fetch Reddit posts
│  ├─ pipeline/            # Processing & feedback pipeline
│  ├─ llm/                 # OpenAI-based extractor
│  ├─ io/                  # S3 & Redshift utilities
│  ├─ quality/             # Data validation (Pandera)
│  └─ services/api/        # FastAPI inference service (real-time)
├─ airflow/dags/main_dag.py # Weekly orchestration (optional)
├─ infra/terraform/         # IaC for S3/IAM/Redshift
├─ tests/                   # Unit + integration tests
├─ docker-compose.yml
├─ Makefile
└─ README.md
```

---

## ⚙️ Setup and Deployment

### Prerequisites

1. **AWS Credentials** (optional, for real cloud run).
2. **Redshift Access** (optional).
3. **Reddit API Credentials** (to fetch posts).
4. **OpenAI API Key** (for extraction).
5. **Docker Installed** (for local demo).
6. **QuickSight** (optional dashboards).

### Environment Variables

Create a `.env` (see `.env.example`):

```env
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_secret
REDDIT_CLIENT_AGENT=featback/1.0
OPENAI_API_KEY=your_openai_key
```

### Local Run (Demo Mode)

```bash
pip install -e .[dev]
pytest
uvicorn featback.services.api.app:app --reload
```

### Batch Run (Single Command)

```bash
python -m featback.pipeline.product_feedback iphone "Iphone 16"
```

### Terraform (IaC Validation)

```bash
cd infra/terraform
terraform init
terraform validate
terraform plan -var="project=featback"
```

---

## ✅ Testing

* **Unit tests** (mocked S3/Reddit/LLM) ensure modules work in isolation.
* **Integration tests** run against a local MinIO + Postgres stack.
* **Pandera schemas** catch malformed data before processing.

Run all tests:

```bash
pytest
```

---

## 🔄 CI/CD

* **Lint + Tests** → runs automatically on every PR with GitHub Actions.
* **Terraform validate/plan** → ensures infra configs are correct.
* **Badges** (add to top of repo once Actions are live):

  * ![CI](https://img.shields.io/github/actions/workflow/status/<your_repo>/ci.yml?branch=main)
  * ![Terraform](https://img.shields.io/github/actions/workflow/status/<your_repo>/terraform.yml?branch=main)

---

## 📸 Screenshots

### Docker Environment

![Pipeline Execution](ProjectScreenshots/docker.png)

### Airflow DAG run

![Dashboard](ProjectScreenshots/airflow.png)

### S3 Data Storage

![Dashboard](ProjectScreenshots/s3.png)

### Redshift Example Query

![Dashboard](ProjectScreenshots/redshift.png)

### QuickSight Visualizations

#### Review Category and Feature Distribution

![Dashboard](ProjectScreenshots/visualization1.png)

#### Sentiment Breakdown and Detailed Tabular View

![Dashboard](ProjectScreenshots/visualization2.png)

#### Sentiment Breakdown over Time

![Dashboard](ProjectScreenshots/visualization3.png)

