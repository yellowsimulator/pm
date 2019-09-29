import { Component, OnInit } from '@angular/core';

declare var Gantt: any;
@Component({
  selector: 'app-ganttchart',
  templateUrl: './ganttchart.component.html',
  styleUrls: ['./ganttchart.component.scss']
})
export class GanttchartComponent implements OnInit {
  ganttitle = 'There we go';
  pipLowerCase = "lowercase";
  pipUpperCase = "uppercase";
  isavailable = true;
  gantt : any;
  tasks: any = [
  {
    id: 'Task 1',
    name: 'Redesign website',
    start: '2016-11-01',
    end: '2016-12-01',
    progress: 90,
  },
  {
    id: 'Task 2',
    name: 'update website',
    start: '2016-12-01',
    end: '2016-12-15',
    dependencies: 'Task 1',
    progress: 10,

  },
]


  constructor() { }

  ngOnInit() {
    this.gantt = new Gantt(".gantt-target", this.tasks);
    this.gantt.change_view_mode('Week')
  }






}
