from torch.utils.tensorboard import SummaryWriter
import time
import os

class Recorder:
    def __init__(self,project_name,lab_name,host_name,hparams = None,record_time=None):
        assert project_name is not None
        assert lab_name is not None
        assert host_name is not None
        self.project_name = project_name
        self.lab_name = lab_name
        self.host_name = host_name
        if record_time is None:
            record_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        record_name = str(project_name) + "_"+str(lab_name) +"_" +str(host_name) +"_" +str(record_time)
        if hparams is not None:
            for key in hparams:
                record_name += ("_"+ str(key) +"_"+str(hparams[key]))
        home_dir = str(os.path.expanduser('~'))+str("/")
        self.writer = SummaryWriter(home_dir + '.tensor_log/'+str(record_name))
        self.avg_save = {}
        self.steps = {}

    def record(self,key,value):
        if key not in self.steps:
            self.steps[key] = 0
        else:
            self.steps[key] += 1
        self.writer.add_scalar(key, value, global_step=self.steps[key], walltime=None)

    def record_avg(self,key,value,times,epoch=None):
        if key not in self.avg_save:
            self.avg_save[key] = {}
            self.avg_save[key]["counter"] = 0
            self.avg_save[key]["sum"] = 0
        self.avg_save[key]["counter"] += 1
        self.avg_save[key]["sum"] += value
        if self.avg_save[key]["counter"] >= times:
            if key not in self.steps:
                self.steps[key] = 0
            else:
                self.steps[key] += 1
            real_value = self.avg_save[key]["sum"]/self.avg_save[key]["counter"]
            print("Recording...")
            self.writer.add_scalar(key,real_value, global_step=self.steps[key], walltime=None)
            if epoch != None:
                self.writer.add_scalar("Epoch",epoch, global_step=self.steps[key], walltime=None)
            self.avg_save[key]["counter"] = 0
            self.avg_save[key]["sum"] = 0
            return real_value
        return None
    
    def record_vector(self,key,vector,bins=200,mask=None):
        if key not in self.steps:
            self.steps[key] = 0
        else:
            self.steps[key] += 1
        if mask is None:
            self.writer.add_histogram(key,values=vector.detach().cpu(),bins=bins,global_step=self.steps[key])
        else:
            mask = mask.squeeze().detach().cpu().bool()
            values = vector.squeeze().detach().cpu()
            values = torch.masked_select(values,mask=mask)
            self.writer.add_histogram(key,values=values,bins=bins,global_step=self.steps[key])

