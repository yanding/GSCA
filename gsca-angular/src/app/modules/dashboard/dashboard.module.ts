import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { DashboardRoutingModule } from './dashboard-routing.module';
import { DashboardComponent } from './dashboard.component';
import { SharedModule } from 'src/app/shared/shared.module';
import { SearchBoxComponent } from './search-box/search-box.component';
import { FeatureDiscriptionComponent } from './feature-discription/feature-discription.component';
import { CitationComponent } from './citation/citation.component';

@NgModule({
  declarations: [DashboardComponent, SearchBoxComponent, FeatureDiscriptionComponent, CitationComponent],
  imports: [CommonModule, DashboardRoutingModule, SharedModule],
})
export class DashboardModule {}
