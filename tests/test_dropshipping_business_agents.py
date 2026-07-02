from app.core.brain import Brain
from app.core.bus.event_bus import EventBus
from app.core.memory import PersistentMemory


class TestLogger:

    def info(self, message):
        pass

    def success(self, message):
        pass

    def warning(self, message):
        pass

    def error(self, message):
        pass


def make_brain(tmp_path):
    memory = PersistentMemory(str(tmp_path / "memory.json"))
    return Brain(TestLogger(), memory, EventBus())


def test_product_research_creates_ranked_candidates(tmp_path):
    brain = make_brain(tmp_path)
    brain.add_supplier_product(
        "Mini LED inteligente sem fios",
        8,
        7,
        "https://supplier.example/mini-led",
        "gadgets"
    )

    result = brain.run_product_research("produto vencedor gadgets")

    assert result["status"] == "product_research_completed"
    assert result["best_candidate"]["campaign_ready"] is True
    assert brain.product_candidates()
    assert brain.best_product_candidate()["candidate"]["score"] >= 60


def test_marketing_and_organic_plans_use_best_candidate(tmp_path):
    brain = make_brain(tmp_path)
    brain.run_product_research("produto vencedor gadgets")

    marketing = brain.create_marketing_plan(platform="Meta Ads")
    organic = brain.create_organic_plan(days=5)

    assert marketing["status"] == "marketing_plan_created"
    assert marketing["platforms"] == ["Meta Ads"]
    assert marketing["headlines"]
    assert marketing["future_campaigns"]

    assert organic["status"] == "organic_plan_created"
    assert len(organic["calendar"]) == 5
    assert organic["short_video_ideas"]


def test_agents_complete_matching_tasks_from_event_bus(tmp_path):
    brain = make_brain(tmp_path)

    organic_task = brain.create_task(
        "criar plano de trafego organico para produto vencedor"
    )
    marketing_task = brain.create_task(
        "criar campanha ads para produto vencedor"
    )

    tasks = brain.tasks.all()

    assert organic_task["status"] == "done"
    assert marketing_task["status"] == "done"
    assert tasks[0]["result"]["status"] == "organic_plan_created"
    assert tasks[1]["result"]["status"] == "marketing_plan_created"
