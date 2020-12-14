import { Component, OnInit, OnChanges, AfterViewInit, SimpleChanges, Input, ViewChild } from '@angular/core';
import { ExpressionApiService } from './../expression-api.service';
import { ExprSearch } from './../../../shared/model/exprsearch';
import collectionList from 'src/app/shared/constants/collectionlist';
import { MatTableDataSource } from '@angular/material/table';
import { GSVATableRecord } from 'src/app/shared/model/gsvatablerecord';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';

@Component({
  selector: 'app-gene-set',
  templateUrl: './gene-set.component.html',
  styleUrls: ['./gene-set.component.css'],
})
export class GeneSetComponent implements OnInit, OnChanges, AfterViewInit {
  @Input() searchTerm: ExprSearch;

  dataSourceGSVALoading = true;
  dataSourceGSVA: MatTableDataSource<GSVATableRecord>;
  showGSVATable = true;
  @ViewChild('paginatorGSVA') paginatorGSVA: MatPaginator;
  @ViewChild(MatSort) sortGSVA: MatSort;
  displayedColumnsGSVA = ['cancertype', 'tumor_gsva', 'normal_gsva', 'log2fc', 'pval'];
  displayedColumnsGSVAHeader = ['Cancer type', 'Tumor GSVA', 'Normal GSVA', 'Fold change', 'P value'];

  GSVAImage: any;
  GSVAPdfURL: string;
  GSVAImageLoading = true;
  showGSVAImage = true;

  constructor(private expressionApiService: ExpressionApiService) {}

  ngOnInit(): void {}

  ngOnChanges(changes: SimpleChanges): void {
    this.dataSourceGSVALoading = true;
    this.GSVAImageLoading = true;
    const postTerm = this._validCollection(this.searchTerm);

    if (!postTerm.validColl.length) {
      this.dataSourceGSVALoading = false;
      this.GSVAImageLoading = false;
      this.showGSVATable = false;
      this.showGSVAImage = false;
    } else {
      this.expressionApiService.getGSVAAnalysis(postTerm).subscribe(
        (res) => {
          this.expressionApiService.getExprGSVAPlot(res.uuidname).subscribe((exprgsvauuids) => {
            this.showGSVATable = true;
            this.expressionApiService.getResourceTable('preanalysised_gsva_expr', exprgsvauuids.exprgsvatableuuid).subscribe(
              (r) => {
                this.dataSourceGSVALoading = false;
                this.dataSourceGSVA = new MatTableDataSource(r);
                this.dataSourceGSVA.paginator = this.paginatorGSVA;
                this.dataSourceGSVA.sort = this.sortGSVA;
              },
              (e) => {
                this.showGSVATable = false;
              }
            );
            this.GSVAPdfURL = this.expressionApiService.getResourcePlotURL(exprgsvauuids.exprgsvaplotuuid, 'pdf');
            this.expressionApiService.getResourcePlotBlob(exprgsvauuids.exprgsvaplotuuid, 'png').subscribe(
              (r) => {
                this.showGSVAImage = true;
                this.GSVAImageLoading = false;
                this._createImageFromBlob(r, 'GSVAImage');
              },
              (e) => {
                this.showGSVAImage = false;
              }
            );
          });
        },
        (err) => {
          this.showGSVATable = false;
          this.showGSVAImage = false;
        }
      );
    }
  }

  ngAfterViewInit(): void {}

  private _validCollection(st: ExprSearch): any {
    st.validColl = st.cancerTypeSelected
      .map((val) => {
        return collectionList.deg.collnames[collectionList.deg.cancertypes.indexOf(val)];
      })
      .filter(Boolean);
    return st;
  }

  private _createImageFromBlob(res: Blob, present: string) {
    const reader = new FileReader();
    reader.addEventListener(
      'load',
      () => {
        switch (present) {
          case 'GSVAImage':
            this.GSVAImage = reader.result;
            break;
        }
      },
      false
    );
    if (res) {
      reader.readAsDataURL(res);
    }
  }

  public applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSourceGSVA.filter = filterValue.trim().toLowerCase();

    if (this.dataSourceGSVA.paginator) {
      this.dataSourceGSVA.paginator.firstPage();
    }
  }
}
