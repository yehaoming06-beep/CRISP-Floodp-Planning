import sys, tempfile, unittest
from pathlib import Path
from dataclasses import replace
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'02_Model'))
from crisp_parameters import load_inputs,derive_upper_bounds
from crisp_model import Runner,PumpFleet

class InventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base=load_inputs(ROOT/'01_Data/CRISP_Master_Data.xlsx')
        cls.temp=tempfile.TemporaryDirectory();cls.runner=Runner(Path(cls.temp.name))
    @classmethod
    def tearDownClass(cls):cls.runner.close();cls.temp.cleanup()
    def synthetic(self):
        p=self.base
        return replace(p,setup_cost={k:0. for k in p.setup_cost},
            benefit={k:10. if k[2]=='Drainage' else 0. for k in p.benefit},
            deploy_cost={k:1. for k in p.benefit},labour={k:1. for k in p.benefit},
            equipment={k:1. for k in p.benefit},supply={k:1. for k in p.benefit},
            operating_budget={s:100. for s in p.scenarios},labour_capacity={s:100. for s in p.scenarios},
            equipment_capacity={s:100. for s in p.scenarios},supply_capacity={s:100. for s in p.scenarios}).with_recomputed_bounds()
    def test_shared_stock_and_reuse_across_scenarios(self):
        p=self.synthetic();f=PumpFleet(1,0,1_000_000,p.locations)
        r=self.runner.solve(p,'shared',f)
        self.assertAlmostEqual(r['objective'],10)
        self.assertEqual(sum(x['x'] for x in r['x'] if x['intervention']=='Drainage'),3)
        self.assertTrue(all(x['used']==1 for x in r['resources'] if x['resource']=='shared_pump_stock'))
    def test_capital_budget_and_integer_purchase(self):
        p=self.synthetic();f=PumpFleet(0,1_999_999,1_000_000,p.locations)
        r=self.runner.solve(p,'capital',f)
        self.assertEqual(r['new_pumps'],1);self.assertAlmostEqual(r['objective'],10)
    def test_eev_fixes_procurement_as_well_as_readiness(self):
        p=self.synthetic();f=PumpFleet(0,2_000_000,1_000_000,p.locations)
        fixed={'y':{k:1 for k in p.setup_cost},'n':0}
        r=self.runner.solve(p,'fixed_n',f,fixed=fixed)
        self.assertEqual(r['new_pumps'],0);self.assertAlmostEqual(r['objective'],0)
        self.assertAlmostEqual(self.runner.solve(p,'free_n',f)['objective'],20)
    def test_no_access_prevents_deployment_and_unnecessary_purchase(self):
        p=self.synthetic();f=PumpFleet(0,2_000_000,1_000_000,())
        r=self.runner.solve(p,'no_access',f)
        self.assertEqual(r['new_pumps'],0);self.assertAlmostEqual(r['objective'],0)
    def test_nonbinding_stock_reproduces_old_model(self):
        a=self.runner.solve(self.base,'old',None)
        b=self.runner.solve(self.base,'unlimited',PumpFleet(100,0,1_000_000,self.base.locations))
        self.assertAlmostEqual(a['objective'],686.0078260869565)
        self.assertAlmostEqual(a['objective'],b['objective']);self.assertEqual(a['plan'],b['plan'])
    def test_derived_bounds_change_with_capacity(self):
        p=self.synthetic();q=replace(p,equipment_capacity={s:200 for s in p.scenarios},
            labour_capacity={s:200 for s in p.scenarios},operating_budget={s:200 for s in p.scenarios},
            supply_capacity={s:200 for s in p.scenarios}).with_recomputed_bounds()
        self.assertEqual(set(p.upper_bound.values()),{100});self.assertEqual(set(q.upper_bound.values()),{200})
        self.assertEqual(derive_upper_bounds(self.base),self.base.upper_bound)
    def test_invalid_inventory_inputs_are_rejected(self):
        with self.assertRaises(ValueError):PumpFleet(None,1,1,self.base.locations).validate(self.base.locations)
        with self.assertRaises(ValueError):PumpFleet(0,1,0,self.base.locations).validate(self.base.locations)

if __name__=='__main__':unittest.main()
