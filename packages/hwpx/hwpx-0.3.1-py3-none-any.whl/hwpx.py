import os
import re

import numpy as np
import pandas as pd
import pythoncom
import win32com.client as win32


class Hwp:
    def __init__(self, new=False, visible=True, register_module=True):
        """
        아래아한글 인스턴스를 실행한다.

        :param new:
            new=True인 경우, 기존에 열려 있는 한/글 인스턴스와 무관한 새 인스턴스를 생성한다.
            new=False(기본값)인 경우, 기존에 열려 있는 한/글 인스턴스를 조작하게 된다.
        :param visible:
            한/글 인스턴스를 백그라운드에서 실행할지, 화면에 나타낼지 선택한다.
            기본값은 True로, 화면에 나타나게 된다.
            visible=False일 경우 백그라운드에서 작업할 수 있다.
        """
        self.hwp = 0
        context = pythoncom.CreateBindCtx(0)

        # 현재 실행중인 프로세스를 가져옵니다.
        running_coms = pythoncom.GetRunningObjectTable()
        monikers = running_coms.EnumRunning()

        if not new:
            for moniker in monikers:
                name = moniker.GetDisplayName(context, moniker)
                # moniker의 DisplayName을 통해 한글을 가져옵니다
                # 한글의 경우 HwpObject.버전으로 각 버전별 실행 이름을 설정합니다.
                if name.startswith('!HwpObject.'):
                    # 120은 한글 2022의 경우입니다.
                    # 현재 moniker를 통해 ROT에서 한글의 object를 가져옵니다.
                    obj = running_coms.GetObject(moniker)
                    # 가져온 object를 Dispatch를 통해 사용할수 있는 객체로 변환시킵니다.
                    self.hwp = win32.gencache.EnsureDispatch(obj.QueryInterface(pythoncom.IID_IDispatch))
                    # 그이후는 오토메이션 api를 사용할수 있습니다
        if not self.hwp:
            self.hwp = win32.gencache.EnsureDispatch("hwpframe.hwpobject")
        self.hwp.XHwpWindows.Item(0).Visible = visible

        # self.Application = self.hwp.Application
        # self.ArcType = self.hwp.ArcType
        # self.AutoNumType = self.hwp.AutoNumType
        # self.BorderShape = self.hwp.BorderShape
        # self.BreakWordLatin = self.hwp.BreakWordLatin
        # self.BrushType = self.hwp.BrushType
        # self.CLSID = self.hwp.CLSID
        # self.Canonical = self.hwp.Canonical
        # self.CellApply = self.hwp.CellApply
        # self.CellShape = self.hwp.CellShape
        # self.CharShadowType = self.hwp.CharShadowType
        # self.CharShape = self.hwp.CharShape
        # self.CheckXObject = self.hwp.CheckXObject
        # self.Clear = self.hwp.Clear
        # self.ColDefType = self.hwp.ColDefType
        # self.ColLayoutType = self.hwp.ColLayoutType
        # self.ConvertPUAHangulToUnicode = self.hwp.ConvertPUAHangulToUnicode
        # self.CreateAction = self.hwp.CreateAction
        # self.CreateField = self.hwp.CreateField
        # self.CreateID = self.hwp.CreateID
        # self.CreateMode = self.hwp.CreateMode
        # self.CreatePageImage = self.hwp.CreatePageImage
        # self.CreateSet = self.hwp.CreateSet
        # self.CrookedSlash = self.hwp.CrookedSlash
        # self.CurFieldState = self.hwp.CurFieldState
        # self.CurMetatagState = self.hwp.CurMetatagState
        # self.CurSelectedCtrl = self.hwp.CurSelectedCtrl
        # self.DSMark = self.hwp.DSMark
        # self.DbfCodeType = self.hwp.DbfCodeType
        # self.DeleteCtrl = self.hwp.DeleteCtrl
        # self.Delimiter = self.hwp.Delimiter
        # self.DrawAspect = self.hwp.DrawAspect
        # self.DrawFillImage = self.hwp.DrawFillImage
        # self.DrawShadowType = self.hwp.DrawShadowType
        # self.EditMode = self.hwp.EditMode
        # self.Encrypt = self.hwp.Encrypt
        # self.EndSize = self.hwp.EndSize
        # self.EndStyle = self.hwp.EndStyle
        # self.EngineProperties = self.hwp.EngineProperties
        # self.ExportStyle = self.hwp.ExportStyle
        # self.FieldExist = self.hwp.FieldExist
        # self.FileTranslate = self.hwp.FileTranslate
        # self.FillAreaType = self.hwp.FillAreaType
        # self.FindCtrl = self.hwp.FindCtrl
        # self.FindDir = self.hwp.FindDir
        # self.FindPrivateInfo = self.hwp.FindPrivateInfo
        # self.FontType = self.hwp.FontType
        # self.GetBinDataPath = self.hwp.GetBinDataPath
        # self.GetCurFieldName = self.hwp.GetCurFieldName
        # self.GetCurMetatagName = self.hwp.GetCurMetatagName
        # self.GetFieldList = self.hwp.GetFieldList
        # self.GetFieldText = self.hwp.GetFieldText
        # self.GetFileInfo = self.hwp.GetFileInfo
        # self.GetFontList = self.hwp.GetFontList
        # self.GetHeadingString = self.hwp.GetHeadingString
        # self.GetMessageBoxMode = self.hwp.GetMessageBoxMode
        # self.GetMetatagList = self.hwp.GetMetatagList
        # self.GetMetatagNameText = self.hwp.GetMetatagNameText
        # self.GetMousePos = self.hwp.GetMousePos
        # self.GetPageText = self.hwp.GetPageText
        # self.GetPos = self.hwp.GetPos
        # self.GetPosBySet = self.hwp.GetPosBySet
        # self.GetScriptSource = self.hwp.GetScriptSource
        # self.GetSelectedPos = self.hwp.GetSelectedPos
        # self.GetSelectedPosBySet = self.hwp.GetSelectedPosBySet
        # self.GetText = self.hwp.GetText
        # self.GetTextFile = self.hwp.GetTextFile
        # self.GetTranslateLangList = self.hwp.GetTranslateLangList
        # self.GetUserInfo = self.hwp.GetUserInfo
        # self.Gradation = self.hwp.Gradation
        # self.GridMethod = self.hwp.GridMethod
        # self.GridViewLine = self.hwp.GridViewLine
        # self.GutterMethod = self.hwp.GutterMethod
        # self.HAction = self.hwp.HAction
        # self.HAlign = self.hwp.HAlign
        # self.HParameterSet = self.hwp.HParameterSet
        # self.Handler = self.hwp.Handler
        # self.Hash = self.hwp.Hash
        # self.HatchStyle = self.hwp.HatchStyle
        # self.HeadCtrl = self.hwp.HeadCtrl
        # self.HeadType = self.hwp.HeadType
        # self.HeightRel = self.hwp.HeightRel
        # self.Hiding = self.hwp.Hiding
        # self.HorzRel = self.hwp.HorzRel
        # self.HwpLineType = self.hwp.HwpLineType
        # self.HwpLineWidth = self.hwp.HwpLineWidth
        # self.HwpOutlineStyle = self.hwp.HwpOutlineStyle
        # self.HwpOutlineType = self.hwp.HwpOutlineType
        # self.HwpUnderlineShape = self.hwp.HwpUnderlineShape
        # self.HwpUnderlineType = self.hwp.HwpUnderlineType
        # self.HwpZoomType = self.hwp.HwpZoomType
        # self.ImageFormat = self.hwp.ImageFormat
        # self.ImportStyle = self.hwp.ImportStyle
        # self.InitHParameterSet = self.hwp.InitHParameterSet
        # self.InitScan = self.hwp.InitScan
        # self.Insert = self.hwp.Insert
        # self.InsertBackgroundPicture = self.hwp.InsertBackgroundPicture
        # self.InsertCtrl = self.hwp.InsertCtrl
        # self.InsertPicture = self.hwp.InsertPicture
        # self.IsActionEnable = self.hwp.IsActionEnable
        # self.IsCommandLock = self.hwp.IsCommandLock
        # self.IsEmpty = self.hwp.IsEmpty
        # self.IsModified = self.hwp.IsModified
        # self.IsPrivateInfoProtected = self.hwp.IsPrivateInfoProtected
        # self.IsTrackChange = self.hwp.IsTrackChange
        # self.IsTrackChangePassword = self.hwp.IsTrackChangePassword
        # self.KeyIndicator = self.hwp.KeyIndicator
        # self.LastCtrl = self.hwp.LastCtrl
        # self.LineSpacingMethod = self.hwp.LineSpacingMethod
        # self.LineWrapType = self.hwp.LineWrapType
        # self.LockCommand = self.hwp.LockCommand
        # self.LunarToSolar = self.hwp.LunarToSolar
        # self.LunarToSolarBySet = self.hwp.LunarToSolarBySet
        # self.MacroState = self.hwp.MacroState
        # self.MailType = self.hwp.MailType
        # self.MetatagExist = self.hwp.MetatagExist
        # self.MiliToHwpUnit = self.hwp.MiliToHwpUnit
        # self.ModifyFieldProperties = self.hwp.ModifyFieldProperties
        # self.ModifyMetatagProperties = self.hwp.ModifyMetatagProperties
        # self.MovePos = self.hwp.MovePos
        # self.MoveToField = self.hwp.MoveToField
        # self.MoveToMetatag = self.hwp.MoveToMetatag
        # self.NumberFormat = self.hwp.NumberFormat
        # self.Numbering = self.hwp.Numbering
        # self.Open = self.hwp.Open
        # self.PageCount = self.hwp.PageCount
        # self.PageNumPosition = self.hwp.PageNumPosition
        # self.PageType = self.hwp.PageType
        # self.ParaHeadAlign = self.hwp.ParaHeadAlign
        # self.ParaShape = self.hwp.ParaShape
        # self.ParentCtrl = self.hwp.ParentCtrl
        # self.Path = self.hwp.Path
        # self.PicEffect = self.hwp.PicEffect
        # self.PlacementType = self.hwp.PlacementType
        # self.PointToHwpUnit = self.hwp.PointToHwpUnit
        # self.PresentEffect = self.hwp.PresentEffect
        # self.PrintDevice = self.hwp.PrintDevice
        # self.PrintPaper = self.hwp.PrintPaper
        # self.PrintRange = self.hwp.PrintRange
        # self.PrintType = self.hwp.PrintType
        # self.ProtectPrivateInfo = self.hwp.ProtectPrivateInfo
        # self.PutFieldText = self.hwp.PutFieldText
        # self.PutMetatagNameText = self.hwp.PutMetatagNameText
        # self.Quit = self.hwp.Quit
        # self.RGBColor = self.hwp.RGBColor
        # self.RegisterModule = self.hwp.RegisterModule
        # self.RegisterPrivateInfoPattern = self.hwp.RegisterPrivateInfoPattern
        # self.ReleaseAction = self.hwp.ReleaseAction
        # self.ReleaseScan = self.hwp.ReleaseScan
        # self.RenameField = self.hwp.RenameField
        # self.RenameMetatag = self.hwp.RenameMetatag
        # self.ReplaceAction = self.hwp.ReplaceAction
        # self.ReplaceFont = self.hwp.ReplaceFont
        # self.Revision = self.hwp.Revision
        # self.Run = self.hwp.Run
        # self.RunScriptMacro = self.hwp.RunScriptMacro
        # self.Save = self.hwp.Save
        # self.SaveAs = self.hwp.SaveAs
        # self.ScanFont = self.hwp.ScanFont
        # self.SelectText = self.hwp.SelectText
        # self.SelectionMode = self.hwp.SelectionMode
        # self.SetBarCodeImage = self.hwp.SetBarCodeImage
        # self.SetCurFieldName = self.hwp.SetCurFieldName
        # self.SetCurMetatagName = self.hwp.SetCurMetatagName
        # self.SetDRMAuthority = self.hwp.SetDRMAuthority
        # self.SetFieldViewOption = self.hwp.SetFieldViewOption
        # self.SetMessageBoxMode = self.hwp.SetMessageBoxMode
        # self.SetPos = self.hwp.SetPos
        # self.SetPosBySet = self.hwp.SetPosBySet
        # self.SetPrivateInfoPassword = self.hwp.SetPrivateInfoPassword
        # self.SetTextFile = self.hwp.SetTextFile
        # self.SetTitleName = self.hwp.SetTitleName
        # self.SetUserInfo = self.hwp.SetUserInfo
        # self.SideType = self.hwp.SideType
        # self.Signature = self.hwp.Signature
        # self.Slash = self.hwp.Slash
        # self.SolarToLunar = self.hwp.SolarToLunar
        # self.SolarToLunarBySet = self.hwp.SolarToLunarBySet
        # self.SortDelimiter = self.hwp.SortDelimiter
        # self.StrikeOut = self.hwp.StrikeOut
        # self.StyleType = self.hwp.StyleType
        # self.SubtPos = self.hwp.SubtPos
        # self.TableBreak = self.hwp.TableBreak
        # self.TableFormat = self.hwp.TableFormat
        # self.TableSwapType = self.hwp.TableSwapType
        # self.TableTarget = self.hwp.TableTarget
        # self.TextAlign = self.hwp.TextAlign
        # self.TextArtAlign = self.hwp.TextArtAlign
        # self.TextDir = self.hwp.TextDir
        # self.TextFlowType = self.hwp.TextFlowType
        # self.TextWrapType = self.hwp.TextWrapType
        # self.UnSelectCtrl = self.hwp.UnSelectCtrl
        # self.VAlign = self.hwp.VAlign
        # self.Version = self.hwp.Version
        # self.VertRel = self.hwp.VertRel
        # self.ViewFlag = self.hwp.ViewFlag
        # self.ViewProperties = self.hwp.ViewProperties
        # self.WatermarkBrush = self.hwp.WatermarkBrush
        # self.WidthRel = self.hwp.WidthRel
        # self.XHwpDocuments = self.hwp.XHwpDocuments
        # self.XHwpMessageBox = self.hwp.XHwpMessageBox
        # self.XHwpODBC = self.hwp.XHwpODBC
        # self.XHwpWindows = self.hwp.XHwpWindows

        if register_module:
            self.register_module()

    @property
    def HeadCtrl(self):
        return self.hwp.HeadCtrl

    @property
    def LastCtrl(self):
        return self.hwp.LastCtrl

    def hwp_unit_to_mili(self, hwp_unit):
        return round(hwp_unit / 7200 * 25.4)

    def create_table(self, rows, cols, treat_as_char=1, width_type=0, height_type=0):
        """
        아래의 148mm는 종이여백 210mm에서 60mm(좌우 각 30mm)를 뺀 150mm에다가,
        표 바깥여백 각 1mm를 뺀 148mm이다. (TableProperties.Width = 41954)
        각 열의 너비는 5개 기준으로 26mm인데 이는 셀마다 안쪽여백 좌우 각각 1.8mm를 뺀 값으로,
        148 - (1.8 x 10 =) 18mm = 130mm
        그래서 셀 너비의 총 합은 130이 되어야 한다.
        아래의 라인28~32까지 셀너비의 합은 16+36+46+16+16=130
        표를 생성하는 시점에는 표 안팎의 여백을 없애거나 수정할 수 없으므로
        이는 고정된 값으로 간주해야 한다.

        :return:
        """
        pset = self.hwp.HParameterSet.HTableCreation
        self.hwp.HAction.GetDefault("TableCreate", pset.HSet)  # 표 생성 시작
        pset.Rows = rows  # 행 갯수
        pset.Cols = cols  # 열 갯수
        pset.WidthType = width_type  # 너비 지정(0:단에맞춤, 1:문단에맞춤, 2:임의값)
        pset.HeightType = height_type  # 높이 지정(0:자동, 1:임의값)

        sec_def = self.hwp.HParameterSet.HSecDef
        self.hwp.HAction.GetDefault("PageSetup", sec_def.HSet)
        total_width = (sec_def.PageDef.PaperWidth - sec_def.PageDef.LeftMargin
                       - sec_def.PageDef.RightMargin - sec_def.PageDef.GutterLen
                       - self.mili_to_hwp_unit(2))

        pset.WidthValue = self.hwp.MiliToHwpUnit(total_width)  # 표 너비
        # pset.HeightValue = self.hwp.MiliToHwpUnit(150)  # 표 높이
        pset.CreateItemArray("ColWidth", cols)  # 열 5개 생성
        each_col_width = total_width - self.mili_to_hwp_unit(3.6 * cols)
        for i in range(cols):
            pset.ColWidth.SetItem(i, self.hwp.MiliToHwpUnit(each_col_width))  # 1열
        pset.TableProperties.TreatAsChar = treat_as_char  # 글자처럼 취급
        pset.TableProperties.Width = total_width  # self.hwp.MiliToHwpUnit(148)  # 표 너비
        self.hwp.HAction.Execute("TableCreate", pset.HSet)  # 위 코드 실행

    def get_sel_text(self):
        self.hwp.InitScan(Range=0xff)
        total_text = ""
        state = 2
        while state not in [0, 1]:
            state, text = self.hwp.GetText()
            total_text += text
        self.hwp.ReleaseScan()
        return total_text

    def table_to_csv(self, idx=1, filename="result.csv"):
        start_pos = self.hwp.GetPos()
        table_num = 0
        ctrl = self.HeadCtrl
        while ctrl.Next:
            if ctrl.UserDesc == "표":
                table_num += 1
            if table_num == idx:
                break
            ctrl = ctrl.Next

        self.hwp.SetPosBySet(ctrl.GetAnchorPos(0))
        self.hwp.FindCtrl()
        self.hwp.HAction.Run("ShapeObjTableSelCell")
        data = [self.get_sel_text()]
        col_count = 1
        while self.hwp.HAction.Run("TableRightCell"):
            # a.append(get_text().replace("\r\n", "\n"))
            if re.match("\([A-Z]1\)", self.hwp.KeyIndicator()[-1]):
                col_count += 1
            data.append(self.get_sel_text())

        array = np.array(data).reshape(col_count, -1)
        df = pd.DataFrame(array[1:], columns=array[0])
        df.to_csv(filename, index=False)
        self.hwp.SetPos(*start_pos)
        print(os.path.join(os.getcwd(), filename))
        return None

    def table_to_df(self, idx=1):
        start_pos = self.hwp.GetPos()
        table_num = 0
        ctrl = self.HeadCtrl
        while ctrl.Next:
            if ctrl.UserDesc == "표":
                table_num += 1
            if table_num == idx:
                break
            ctrl = ctrl.Next

        self.hwp.SetPosBySet(ctrl.GetAnchorPos(0))
        self.hwp.FindCtrl()
        self.hwp.HAction.Run("ShapeObjTableSelCell")
        data = [self.get_sel_text()]
        col_count = 1
        while self.hwp.HAction.Run("TableRightCell"):
            # a.append(get_text().replace("\r\n", "\n"))
            if re.match("\([A-Z]1\)", self.hwp.KeyIndicator()[-1]):
                col_count += 1
            data.append(self.get_sel_text())

        array = np.array(data).reshape(col_count, -1)
        df = pd.DataFrame(array[1:], columns=array[0])
        self.hwp.SetPos(*start_pos)
        return df

    def insert_text(self, text):
        param = self.hwp.HParameterSet.HInsertText
        self.hwp.HAction.GetDefault("InsertText", param.HSet)
        param.Text = text
        self.hwp.HAction.Execute("InsertText", param.HSet)

    def move_caption(self, location="Bottom"):
        start_pos = self.hwp.GetPos()
        ctrl = self.HeadCtrl
        while ctrl:
            if ctrl.UserDesc == "번호 넣기":
                self.hwp.SetPosBySet(ctrl.GetAnchorPos(0))
                self.hwp.HAction.Run("ParagraphShapeAlignCenter")
                param = self.hwp.HParameterSet.HShapeObject
                self.hwp.HAction.GetDefault("TablePropertyDialog", param.HSet)
                param.ShapeCaption.Side = self.hwp.SideType(location)
                self.hwp.HAction.Execute("TablePropertyDialog", param.HSet)
            ctrl = ctrl.Next
        self.hwp.SetPos(*start_pos)
        return None

    def is_empty(self) -> bool:
        """
        아무 내용도 들어있지 않은 빈 문서인지 여부를 나타낸다. 읽기전용
        """
        return self.hwp.IsEmpty

    def is_modified(self) -> bool:
        """
        최근 저장 또는 생성 이후 수정이 있는지 여부를 나타낸다. 읽기전용
        """
        return self.hwp.IsModified

    def arc_type(self, arc_type):
        return self.hwp.ArcType(ArcType=arc_type)

    def auto_num_type(self, autonum):
        return self.hwp.AutoNumType(autonum=autonum)

    def border_shape(self, border_type):
        return self.hwp.BorderShape(BorderType=border_type)

    def break_word_latin(self, break_latin_word):
        return self.hwp.BreakWordLatin(BreakLatinWord=break_latin_word)

    def brush_type(self, brush_type):
        return self.hwp.BrushType(BrushType=brush_type)

    def canonical(self, canonical):
        return self.hwp.Canonical(Canonical=canonical)

    def cell_apply(self, cell_apply):
        return self.hwp.CellApply(CellApply=cell_apply)

    def char_shadow_type(self, shadow_type):
        return self.hwp.CharShadowType(ShadowType=shadow_type)

    def check_xobject(self, bstring):
        return self.hwp.CheckXObject(bstring=bstring)

    def clear(self, option: int = 1):
        """
        현재 편집중인 문서의 내용을 닫고 빈문서 편집 상태로 돌아간다.

        :param option:
            편집중인 문서의 내용에 대한 처리 방법, 생략하면 1(hwpDiscard)가 선택된다.
            0: 문서의 내용이 변경되었을 때 사용자에게 저장할지 묻는 대화상자를 띄운다. (hwpAskSave)
            1: 문서의 내용을 버린다. (hwpDiscard, 기본값)
            2: 문서가 변경된 경우 저장한다. (hwpSaveIfDirty)
            3: 무조건 저장한다. (hwpSave)

        :return:
            None

        :examples:
            >>> self.hwp.clear(1)
        """
        return self.hwp.Clear(option=option)

    def col_def_type(self, col_def_type):
        return self.hwp.ColDefType(ColDefType=col_def_type)

    def col_layout_type(self, col_layout_type):
        return self.hwp.ColLayoutType(ColLayoutType=col_layout_type)

    def convert_pua_hangul_to_unicode(self, reverse):
        return self.hwp.ConvertPUAHangulToUnicode(Reverse=reverse)

    def create_action(self, actidstr: str):
        """
        Action 객체를 생성한다.
        액션에 대한 세부적인 제어가 필요할 때 사용한다.
        예를 들어 기능을 수행하지 않고 대화상자만을 띄운다든지,
        대화상자 없이 지정한 옵션에 따라 기능을 수행하는 등에 사용할 수 있다.

        :param actidstr:
            액션 ID (ActionIDTable.hwp 참조)

        :return:
            Action object

        :examples:
            >>> # 현재 커서의 폰트 크기(Height)를 구하는 코드
            >>> act = self.hwp.CreateAction("CharShape")
            >>> cs = act.CreateSet()  # == cs = self.hwp.CreateSet(act)
            >>> act.GetDefault(cs)
            >>> print(cs.Item("Height"))
            2800

            >>> # 현재 선택범위의 폰트 크기를 20pt로 변경하는 코드
            >>> act = self.hwp.CreateAction("CharShape")
            >>> cs = act.CreateSet()  # == cs = self.hwp.CreateSet(act)
            >>> act.GetDefault(cs)
            >>> cs.SetItem("Height", self.hwp.PointToHwpUnit(20))
            >>> act.Execute(cs)
            True

        """
        return self.hwp.CreateAction(actidstr=actidstr)

    def create_field(self, name: str, direction: str = "", memo: str = "") -> bool:
        """
        캐럿의 현재 위치에 누름틀을 생성한다.

        :param direction:
            누름틀에 입력이 안 된 상태에서 보이는 안내문/지시문.

        :param memo:
            누름틀에 대한 설명/도움말

        :param name:
            누름틀 필드에 대한 필드 이름(중요)

        :return:
            성공이면 True, 실패면 False

        :examples:
            >>> self.hwp.create_field(direction="이름", memo="이름을 입력하는 필드", name="name")
            True
            >>> self.hwp.PutFieldText("name", "일코")
        """
        return self.hwp.CreateField(Direction=direction, memo=memo, name=name)

    def create_id(self, creation_id):
        return self.hwp.CreateID(CreationID=creation_id)

    def create_mode(self, creation_mode):
        return self.hwp.CreateMode(CreationMode=creation_mode)

    def create_page_image(self, path: str, pgno: int = 0, resolution: int = 300, depth: int = 24,
                          format: str = "bmp") -> bool:
        """
        지정된 페이지를 이미지파일로 저장한다.
        저장되는 이미지파일의 포맷은 비트맵 또는 GIF 이미지이다.
        만약 이 외의 포맷이 입력되었다면 비트맵으로 저장한다.

        :param path:
            생성할 이미지 파일의 경로(전체경로로 입력해야 함)

        :param pgno:
            페이지 번호. 0부터 PageCount-1 까지. 생략하면 0이 사용된다.
            페이지 복수선택은 불가하므로,
            for나 while 등 반복문을 사용해야 한다.

        :param resolution:
            이미지 해상도. DPI단위(96, 300, 1200 등)로 지정한다.
            생략하면 300이 사용된다.

        :param depth:
            이미지파일의 Color Depth(1, 4, 8, 24)를 지정한다.
            생략하면 24

        :param format:
            이미지파일의 포맷. "bmp", "gif"중의 하나. 생략하면 "bmp"가 사용된다.

        :return:
            성공하면 True, 실패하면 False

        examples:
            >>> self.hwp.create_page_image("c:/Users/User/Desktop/a.bmp")
            True
        """
        return self.hwp.CreatePageImage(Path=path, pgno=pgno, resolution=resolution, depth=depth, Format=format)

    def create_set(self, setidstr):
        """
        ParameterSet을 생성한다.
        단독으로 쓰이는 경우는 거의 없으며,
        대부분 create_action과 같이 사용한다.

        ParameterSet은 일종의 정보를 지니는 객체이다.
        어떤 Action들은 그 Action이 수행되기 위해서 정보가 필요한데
        이 때 사용되는 정보를 ParameterSet으로 넘겨준다.
        또한 한/글 컨트롤은 특정정보(ViewProperties, CellShape, CharShape 등)를
        ParameterSet으로 변환하여 넘겨주기도 한다.
        사용 가능한 ParameterSet의 ID는 ParameterSet Table.hwp문서를 참조한다.

        :param setidstr:
            생성할 ParameterSet의 ID (ParameterSet Table.hwp 참고)

        :return:
            생성된 ParameterSet Object
        """
        return self.hwp.CreateSet(setidstr=setidstr)

    def crooked_slash(self, crooked_slash):
        return self.hwp.CrookedSlash(CrookedSlash=crooked_slash)

    def ds_mark(self, diac_sym_mark):
        return self.hwp.DSMark(DiacSymMark=diac_sym_mark)

    def dbf_code_type(self, dbf_code):
        return self.hwp.DbfCodeType(DbfCode=dbf_code)

    def delete_ctrl(self, ctrl) -> bool:
        """
        문서 내 컨트롤을 삭제한다.

        :param ctrl:
            삭제할 문서 내 컨트롤

        :return:
            성공하면 True, 실패하면 False

        examples:
            >>> ctrl = self.hwp.HeadCtrl.Next.Next
            >>> if ctrl.UserDesc == "표":
            ...     self.hwp.delete_ctrl(ctrl)
            ...
            True
        """
        return self.hwp.DeleteCtrl(ctrl=ctrl)

    def delimiter(self, delimiter):
        return self.hwp.Delimiter(Delimiter=delimiter)

    def draw_aspect(self, draw_aspect):
        return self.hwp.DrawAspect(DrawAspect=draw_aspect)

    def draw_fill_image(self, fillimage):
        return self.hwp.DrawFillImage(fillimage=fillimage)

    def draw_shadow_type(self, shadow_type):
        return self.hwp.DrawShadowType(ShadowType=shadow_type)

    def encrypt(self, encrypt):
        return self.hwp.Encrypt(Encrypt=encrypt)

    def end_size(self, end_size):
        return self.hwp.EndSize(EndSize=end_size)

    def end_style(self, end_style):
        return self.hwp.EndStyle(EndStyle=end_style)

    def export_style(self, sty_filepath: str) -> bool:
        """
        현재 문서의 Style을 sty 파일로 Export한다.

        :param sty_filepath:
            Export할 sty 파일의 전체경로 문자열

        :return:
            성공시 True, 실패시 False

        :Examples
            >>> self.hwp.export_style("C:/Users/User/Desktop/new_style.sty")
            True
        """
        style_set = self.hwp.HParameterSet.HStyleTemplate
        style_set.filename = sty_filepath
        return self.hwp.ExportStyle(param=style_set.HSet)

    def field_exist(self, field):
        """
        문서에 지정된 데이터 필드가 존재하는지 검사한다.

        :param field:
            필드이름

        :return:
            필드가 존재하면 True, 존재하지 않으면 False
        """
        return self.hwp.FieldExist(Field=field)

    def file_translate(self, cur_lang, trans_lang):
        return self.hwp.FileTranslate(curLang=cur_lang, transLang=trans_lang)

    def fill_area_type(self, fill_area):
        return self.hwp.FillAreaType(FillArea=fill_area)

    def find_ctrl(self):
        return self.hwp.FindCtrl()

    def find_dir(self, find_dir):
        return self.hwp.FindDir(FindDir=find_dir)

    def find_private_info(self, private_type, private_string):
        """
        개인정보를 찾는다.
        (비밀번호 설정 등의 이유, 현재 비활성화된 것으로 추정)

        :param private_type:
            보호할 개인정보 유형. 다음의 값을 하나이상 조합한다.
            0x0001: 전화번호
            0x0002: 주민등록번호
            0x0004: 외국인등록번호
            0x0008: 전자우편
            0x0010: 계좌번호
            0x0020: 신용카드번호
            0x0040: IP 주소
            0x0080: 생년월일
            0x0100: 주소
            0x0200: 사용자 정의
            0x0400: 기타

        :param private_string:
            기타 문자열. 예: "신한카드"
            0x0400 유형이 존재할 경우에만 유효하므로, 생략가능하다

        :return:
            찾은 개인정보의 유형 값. 다음과 같다.
            0x0001 : 전화번호
            0x0002 : 주민등록번호
            0x0004 : 외국인등록번호
            0x0008 : 전자우편
            0x0010 : 계좌번호
            0x0020 : 신용카드번호
            0x0040 : IP 주소
            0x0080 : 생년월일
            0x0100 : 주소
            0x0200 : 사용자 정의
            0x0400 : 기타
            개인정보가 없는 경우에는 0을 반환한다.
            또한, 검색 중 문서의 끝(end of document)을 만나면 –1을 반환한다. 이는 함수가 무한히 반복하는 것을 막아준다.
        """
        return self.hwp.FindPrivateInfo(PrivateType=private_type, PrivateString=private_string)

    def font_type(self, font_type):
        return self.hwp.FontType(FontType=font_type)

    def get_bin_data_path(self, binid):
        """
        Binary Data(Temp Image 등)의 경로를 가져온다.

        :param binid:
            바이너리 데이터의 ID 값 (1부터 시작)

        :return:
            바이너리 데이터의 경로

        Examples:
            >>> path = self.hwp.GetBinDataPath(2)
            >>> print(path)
            C:/Users/User/AppData/Local/Temp/Hnc/BinData/EMB00004dd86171.jpg
        """
        return self.hwp.GetBinDataPath(binid=binid)

    def get_cur_field_name(self, option=0):
        """
        현재 캐럿이 위치하는 곳의 필드이름을 구한다.
        이 함수를 통해 현재 필드가 셀필드인지 누름틀필드인지 구할 수 있다.
        참고로, 필드 좌측에 커서가 붙어있을 때는 이름을 구할 수 있지만,
        우측에 붙어 있을 때는 작동하지 않는다.
        GetFieldList()의 옵션 중에 hwpFieldSelection(=4)옵션은 사용하지 않는다.


        :param option:
            다음과 같은 옵션을 지정할 수 있다.
            0: 모두 off. 생략하면 0이 지정된다.
            1: 셀에 부여된 필드 리스트만을 구한다. hwpFieldClickHere와는 함께 지정할 수 없다.(hwpFieldCell)
            2: 누름틀에 부여된 필드 리스트만을 구한다. hwpFieldCell과는 함께 지정할 수 없다.(hwpFieldClickHere)

        :return:
            필드이름이 돌아온다.
            필드이름이 없는 경우 빈 문자열이 돌아온다.
        """
        return self.hwp.GetCurFieldName(option=option)

    def get_cur_metatag_name(self):
        return self.hwp.GetCurMetatagName()

    def get_field_list(self, number=0, option=0):
        """
        문서에 존재하는 필드의 목록을 구한다.
        문서 중에 동일한 이름의 필드가 여러 개 존재할 때는
        number에 지정한 타입에 따라 3 가지의 서로 다른 방식 중에서 선택할 수 있다.
        예를 들어 문서 중 title, body, title, body, footer 순으로
        5개의 필드가 존재할 때, hwpFieldPlain, hwpFieldNumber, HwpFieldCount
        세 가지 형식에 따라 다음과 같은 내용이 돌아온다.
        hwpFieldPlain: "title\x02body\x02title\x02body\x02footer"
        hwpFieldNumber: "title{{0}}\x02body{{0}}\x02title{{1}}\x02body{{1}}\x02footer{{0}}"
        hwpFieldCount: "title{{2}}\x02body{{2}}\x02footer{{1}}"

        :param number:
            문서 내에서 동일한 이름의 필드가 여러 개 존재할 경우
            이를 구별하기 위한 식별방법을 지정한다.
            생략하면 0(hwpFieldPlain)이 지정된다.
            0: 아무 기호 없이 순서대로 필드의 이름을 나열한다.(hwpFieldPlain)
            1: 필드이름 뒤에 일련번호가 {{#}}과 같은 형식으로 붙는다.(hwpFieldNumber)
            2: 필드이름 뒤에 그 필드의 개수가 {{#}}과 같은 형식으로 붙는다.(hwpFieldCount)

        :param option:
            다음과 같은 옵션을 조합할 수 있다. 0을 지정하면 모두 off이다.
            생략하면 0이 지정된다.
            0x01: 셀에 부여된 필드 리스트만을 구한다. hwpFieldClickHere과는 함께 지정할 수 없다.(hwpFieldCell)
            0x02: 누름틀에 부여된 필드 리스트만을 구한다. hwpFieldCell과는 함께 지정할 수 없다.(hwpFieldClickHere)
            0x04: 선택된 내용 안에 존재하는 필드 리스트를 구한다.(HwpFieldSelection)

        :return:
            각 필드 사이를 문자코드 0x02로 구분하여 다음과 같은 형식으로 리턴 한다.
            (가장 마지막 필드에는 0x02가 붙지 않는다.)
            "필드이름#1\x02필드이름#2\x02...필드이름#n"
        """
        return self.hwp.GetFieldList(Number=number, option=option)

    def get_field_text(self, field):
        """
        지정한 필드에서 문자열을 구한다.


        :param field:
            텍스트를 구할 필드 이름의 리스트.
            다음과 같이 필드 사이를 문자 코드 0x02로 구분하여
            한 번에 여러 개의 필드를 지정할 수 있다.
            "필드이름#1\x02필드이름#2\x02...필드이름#n"
            지정한 필드 이름이 문서 중에 두 개 이상 존재할 때의 표현 방식은 다음과 같다.
            "필드이름": 이름의 필드 중 첫 번째
            "필드이름{{n}}": 지정한 이름의 필드 중 n 번째
            예를 들어 "제목{{1}}\x02본문\x02이름{{0}}" 과 같이 지정하면
            '제목'이라는 이름의 필드 중 두 번째,
            '본문'이라는 이름의 필드 중 첫 번째,
            '이름'이라는 이름의 필드 중 첫 번째를 각각 지정한다.
            즉, '필드이름'과 '필드이름{{0}}'은 동일한 의미로 해석된다.

        :return:
            텍스트 데이터가 돌아온다.
            텍스트에서 탭은 '\t'(0x9),
            문단 바뀜은 CR/LF(0x0D/0x0A == \r\n)로 표현되며,
            이외의 특수 코드는 포함되지 않는다.
            필드 텍스트의 끝은 0x02(\x02)로 표현되며,
            그 이후 다음 필드의 텍스트가 연속해서
            지정한 필드 리스트의 개수만큼 위치한다.
            지정한 이름의 필드가 없거나,
            사용자가 해당 필드에 아무 텍스트도 입력하지 않았으면
            해당 텍스트에는 빈 문자열이 돌아온다.
        """
        return self.hwp.GetFieldText(Field=field)

    def get_file_info(self, filename):
        """
        파일 정보를 알아낸다.
        한글 문서를 열기 전에 암호가 걸린 문서인지 확인할 목적으로 만들어졌다.
        (현재 한/글2022 기준으로 hwpx포맷에 대해서는 파일정보를 파악할 수 없다.)

        :param filename:
            정보를 구하고자 하는 hwp 파일의 전체 경로

        :return:
            "FileInfo" ParameterSet이 반환된다.
            파라미터셋의 ItemID는 아래와 같다.
            Format(string) : 파일의 형식.(HWP : 한/글 파일, UNKNOWN : 알 수 없음.)
            VersionStr(string) : 파일의 버전 문자열. ex)5.0.0.3
            VersionNum(unsigned int) : 파일의 버전. ex) 0x05000003
            Encrypted(int) : 암호 여부 (현재는 파일 버전 3.0.0.0 이후 문서-한/글97, 한/글 워디안 및 한/글 2002 이상의 버전-에 대해서만 판단한다.)
            (-1: 판단할 수 없음, 0: 암호가 걸려 있지 않음, 양수: 암호가 걸려 있음.)

        Examples:
            >>> pset = self.hwp.GetFileInfo("C:/Users/Administrator/Desktop/이력서.hwp")
            >>> print(pset.Item("Format"))
            >>> print(pset.Item("VersionStr"))
            >>> print(hex(pset.Item("VersionNum")))
            >>> print(pset.Item("Encrypted"))
            HWP
            5.1.1.0
            0x5010100
            0
        """
        return self.hwp.GetFileInfo(filename=filename)

    def get_font_list(self, langid):
        self.scan_font()
        return self.hwp.GetFontList(langid=langid)

    def get_heading_string(self):
        """
        현재 커서가 위치한 문단의 글머리표/문단번호/개요번호를 추출한다.
        글머리표/문단번호/개요번호가 있는 경우, 해당 문자열을 얻어올 수 있다.
        문단에 글머리표/문단번호/개요번호가 없는 경우, 빈 문자열이 추출된다.

        :return:
            (글머리표/문단번호/개요번호가 있다면) 해당 문자열이 반환된다.
        """
        return self.hwp.GetHeadingString()

    def get_message_box_mode(self):
        """
        현재 메시지 박스의 Mode를 int로 얻어온다.
        set_message_box_mode와 함께 쓰인다.
        6개의 대화상자에서 각각 확인/취소/종료/재시도/무시/예/아니오 버튼을
        자동으로 선택할 수 있게 설정할 수 있으며 조합 가능하다.

        :return:
            // 메시지 박스의 종류
            MB_MASK: 0x00FFFFFF
            // 1. 확인(MB_OK) : IDOK(1)
            MB_OK_IDOK: 0x00000001
            MB_OK_MASK: 0x0000000F
            // 2. 확인/취소(MB_OKCANCEL) : IDOK(1), IDCANCEL(2)
            MB_OKCANCEL_IDOK: 0x00000010
            MB_OKCANCEL_IDCANCEL: 0x00000020
            MB_OKCANCEL_MASK: 0x000000F0
            // 3. 종료/재시도/무시(MB_ABORTRETRYIGNORE) : IDABORT(3), IDRETRY(4), IDIGNORE(5)
            MB_ABORTRETRYIGNORE_IDABORT: 0x00000100
            MB_ABORTRETRYIGNORE_IDRETRY: 0x00000200
            MB_ABORTRETRYIGNORE_IDIGNORE: 0x00000400
            MB_ABORTRETRYIGNORE_MASK: 0x00000F00
            // 4. 예/아니오/취소(MB_YESNOCANCEL) : IDYES(6), IDNO(7), IDCANCEL(2)
            MB_YESNOCANCEL_IDYES: 0x00001000
            MB_YESNOCANCEL_IDNO: 0x00002000
            MB_YESNOCANCEL_IDCANCEL: 0x00004000
            MB_YESNOCANCEL_MASK: 0x0000F000
            // 5. 예/아니오(MB_YESNO) : IDYES(6), IDNO(7)
            MB_YESNO_IDYES: 0x00010000
            MB_YESNO_IDNO: 0x00020000
            MB_YESNO_MASK: 0x000F0000
            // 6. 재시도/취소(MB_RETRYCANCEL) : IDRETRY(4), IDCANCEL(2)
            MB_RETRYCANCEL_IDRETRY: 0x00100000
            MB_RETRYCANCEL_IDCANCEL: 0x00200000
            MB_RETRYCANCEL_MASK: 0x00F00000
        """
        return self.hwp.GetMessageBoxMode()

    def get_metatag_list(self, number, option):
        return self.hwp.GetMetatagList(Number=number, option=option)

    def get_metatag_name_text(self, tag):
        return self.hwp.GetMetatagNameText(tag=tag)

    def get_mouse_pos(self, x_rel_to=1, y_rel_to=1):
        """
        마우스의 현재 위치를 얻어온다.
        단위가 HWPUNIT임을 주의해야 한다.
        (1 inch = 7200 HWPUNIT, 1mm = 283.465 HWPUNIT)

        :param x_rel_to:
            X좌표계의 기준 위치(기본값은 1:쪽기준)
            0: 종이 기준으로 좌표를 가져온다.
            1: 쪽 기준으로 좌표를 가져온다.

        :param y_rel_to:
            Y좌표계의 기준 위치(기본값은 1:쪽기준)
            0: 종이 기준으로 좌표를 가져온다.
            1: 쪽 기준으로 좌표를 가져온다.

        :return:
            "MousePos" ParameterSet이 반환된다.
            아이템ID는 아래와 같다.
            XRelTo(unsigned long): 가로 상대적 기준(0: 종이, 1: 쪽)
            YRelTo(unsigned long): 세로 상대적 기준(0: 종이, 1: 쪽)
            Page(unsigned long): 페이지 번호(0-based)
            X(long): 가로 클릭한 위치(HWPUNIT)
            Y(long): 세로 클릭한 위치(HWPUNIT)

        Examples:
            >>> pset = self.hwp.GetMousePos(1, 1)
            >>> print("X축 기준:", "쪽" if pset.Item("XRelTo") else "종이")
            >>> print("Y축 기준:", "쪽" if pset.Item("YRelTo") else "종이")
            >>> print("현재", pset.Item("Page")+1, "페이지에 커서 위치")
            >>> print("좌상단 기준 우측으로", int(pset.Item("X") / 283.465), "mm에 위치")
            >>> print("좌상단 기준 아래로", int(pset.Item("Y") / 283.465), "mm에 위치")
            X축 기준: 쪽
            Y축 기준: 쪽
            현재 2 페이지에 커서 위치
            좌상단 기준 우측으로 79 mm에 위치
            좌상단 기준 아래로 217 mm에 위치
        """
        return self.hwp.GetMousePos(XRelTo=x_rel_to, YRelTo=y_rel_to)

    def get_page_text(self, pgno: int = 0, option: hex = 0xffffffff) -> str:
        """
        페이지 단위의 텍스트 추출
        일반 텍스트(글자처럼 취급 도형 포함)를 우선적으로 추출하고,
        도형(표, 글상자) 내의 텍스트를 추출한다.
        팁: get_text로는 글머리를 추출하지 않지만, get_page_text는 추출한다.
        팁2: 아무리 get_page_text라도 유일하게 표번호는 추출하지 못한다.
        표번호는 XML태그 속성 안에 저장되기 때문이다.

        :param pgno:
            텍스트를 추출 할 페이지의 번호(0부터 시작)

        :param option:
            추출 대상을 다음과 같은 옵션을 조합하여 지정할 수 있다.
            생략(또는 0xffffffff)하면 모든 텍스트를 추출한다.
            0x00: 본문 텍스트만 추출한다.(maskNormal)
            0x01: 표에대한 텍스트를 추출한다.(maskTable)
            0x02: 글상자 텍스트를 추출한다.(maskTextbox)
            0x04: 캡션 텍스트를 추출한다. (표, ShapeObject)(maskCaption)

        :return:
            해당 페이지의 텍스트가 추출된다.
            글머리는 추출하지만, 표번호는 추출하지 못한다.
        """
        return self.hwp.GetPageText(pgno=pgno, option=option)

    def get_pos(self) -> tuple[int]:
        """
        캐럿의 위치를 얻어온다.
        파라미터 중 리스트는, 문단과 컨트롤들이 연결된 한/글 문서 내 구조를 뜻한다.
        리스트 아이디는 문서 내 위치 정보 중 하나로서 SelectText에 넘겨줄 때 사용한다.
        (파이썬 자료형인 list가 아님)

        :return:
            (List, para, pos) 튜플.
            list: 캐럿이 위치한 문서 내 list ID(본문이 0)
            para: 캐럿이 위치한 문단 ID(0부터 시작)
            pos: 캐럿이 위치한 문단 내 글자 위치(0부터 시작)

        """
        return self.hwp.GetPos()

    def get_pos_by_set(self):
        """
        현재 캐럿의 위치 정보를 ParameterSet으로 얻어온다.
        해당 파라미터셋은 set_pos_by_set에 직접 집어넣을 수 있어 간편히 사용할 수 있다.

        :return:
            캐럿 위치에 대한 ParameterSet
            해당 파라미터셋의 아이템은 아래와 같다.
            "List": 캐럿이 위치한 문서 내 list ID(본문이 0)
            "Para": 캐럿이 위치한 문단 ID(0부터 시작)
            "Pos": 캐럿이 위치한 문단 내 글자 위치(0부터 시작)

        Examples:
            >>> pset = self.hwp.get_pos_by_set()  # 캐럿위치 저장
            >>> print(pset.Item("List"))
            6
            >>> print(pset.Item("Para"))
            3
            >>> print(pset.Item("Pos"))
            2
            >>> self.hwp.set_pos_by_set(pset)  # 캐럿위치 복원
            True
        """
        return self.hwp.GetPosBySet()

    def get_script_source(self, filename: str) -> str:
        """
        문서에 포함된 매크로(스크립트매크로 제외) 소스코드를 가져온다.
        문서포함 매크로는 기본적으로
        ```
        function OnDocument_New() {
        }
        function OnDocument_Open() {
        }
        ```
        형태로 비어있는 상태이며,
        OnDocument_New와 OnDocument_Open 두 개의 함수에 한해서만
        코드를 추가하고 실행할 수 있다.

        :param filename:
            매크로 소스를 가져올 한/글 문서의 전체경로

        :return:
            (문서에 포함된) 스크립트의 소스코드

        Examples:
            >>> print(hwp.get_script_source("C:/Users/User/Desktop/script.hwp"))
            function OnDocument_New()
            {
                HAction.GetDefault("InsertText", HParameterSet.HInsertText.HSet);
                HParameterSet.HInsertText.Text = "ㅁㄴㅇㄹㅁㄴㅇㄹ";
                HAction.Execute("InsertText", HParameterSet.HInsertText.HSet);
            }
            function OnDocument_Open()
            {
                HAction.GetDefault("InsertText", HParameterSet.HInsertText.HSet);
                HParameterSet.HInsertText.Text = "ㅋㅌㅊㅍㅋㅌㅊㅍ";
                HAction.Execute("InsertText", HParameterSet.HInsertText.HSet);
            }
        """
        return self.hwp.GetScriptSource(filename=filename)

    def get_selected_pos(self):
        """
        현재 설정된 블록의 위치정보를 얻어온다.

        :return:
            블록상태여부, 시작과 끝위치 인덱스인 6개 정수 등 7개 요소의 튜플을 리턴
            (is_block, slist, spara, spos, elist, epara, epos)
            is_block: 현재 블록선택상태 여부(블록상태이면 True)
            slist: 설정된 블록의 시작 리스트 아이디.
            spara: 설정된 블록의 시작 문단 아이디.
            spos: 설정된 블록의 문단 내 시작 글자 단위 위치.
            elist: 설정된 블록의 끝 리스트 아이디.
            epara: 설정된 블록의 끝 문단 아이디.
            epos: 설정된 블록의 문단 내 끝 글자 단위 위치.

        Examples:
            >>> self.hwp.get_selected_pos()
            (True, 0, 0, 16, 0, 7, 16)
        """
        return self.hwp.GetSelectedPos()

    def get_selected_pos_by_set(self, sset, eset):
        """
        현재 설정된 블록의 위치정보를 얻어온다.
        (GetSelectedPos의 ParameterSet버전)
        실행 전 GetPos 형태의 파라미터셋 두 개를 미리 만들어서
        인자로 넣어줘야 한다.

        :param sset:
            설정된 블록의 시작 파라메터셋 (ListParaPos)

        :param eset:
            설정된 블록의 끝 파라메터셋 (ListParaPos)

        :return:
            성공하면 True, 실패하면 False.
            실행시 sset과 eset의 아이템 값이 업데이트된다.

        Examples:
            >>> sset = self.hwp.get_pos_by_set()
            >>> eset = self.hwp.get_pos_by_set()
            >>> self.hwp.GetSelectedPosBySet(sset, eset)
            >>> self.hwp.SetPosBySet(eset)
            True
        """
        return self.hwp.GetSelectedPosBySet(sset=sset, eset=eset)

    def get_text(self):
        """
        문서 내에서 텍스트를 얻어온다.
        줄바꿈 기준으로 텍스트를 얻어오므로 반복실행해야 한다.
        get_text()의 사용이 끝나면 release_scan()을 반드시 호출하여
        관련 정보를 초기화 해주어야 한다.
        get_text()로 추출한 텍스트가 있는 문단으로 캐럿을 이동 시키려면
        move_pos(201)을 실행하면 된다.

        :return:
            (state: int, text: str) 형태의 튜플을 리턴한다.
            state의 의미는 아래와 같다.
            0: 텍스트 정보 없음
            1: 리스트의 끝
            2: 일반 텍스트
            3: 다음 문단
            4: 제어문자 내부로 들어감
            5: 제어문자를 빠져나옴
            101: 초기화 안 됨(init_scan() 실패 또는 init_scan()을 실행하지 않은 경우)
            102: 텍스트 변환 실패
            text는 추출한 텍스트 데이터이다.
            텍스트에서 탭은 '\t'(0x9), 문단 바뀜은 '\r\n'(0x0D/0x0A)로 표현되며,
            이외의 특수 코드는 포함되지 않는다.

        Examples:
            >>> self.hwp.init_scan()
            >>> while True:
            ...     state, text = self.hwp.get_text()
            ...     print(state, text)
            ...     if state <= 1:
            ...         break
            ... self.hwp.release_scan()
            2
            2
            2 ㅁㄴㅇㄹ
            3
            4 ㅂㅈㄷㄱ
            2 ㅂㅈㄷㄱ
            5
            1

        """
        return self.hwp.GetText()

    def get_text_file(self, format="UNICODE", option=""):
        """
        현재 열린 문서를 문자열로 넘겨준다.
        이 함수는 JScript나 VBScript와 같이
        직접적으로 local disk를 접근하기 힘든 언어를 위해 만들어졌으므로
        disk를 접근할 수 있는 언어에서는 사용하지 않기를 권장.
        disk를 접근할 수 있다면, Save나 SaveBlockAction을 사용할 것.
        이 함수 역시 내부적으로는 save나 SaveBlockAction을 호출하도록 되어있고
        텍스트로 저장된 파일이 메모리에서 3~4번 복사되기 때문에 느리고,
        메모리를 낭비함.
        팁: HTML로 추출시 표번호가 유지된다.

        :param format:
            파일의 형식. 기본값은 "UNICODE"
            "HWP": HWP native format, BASE64로 인코딩되어 있다. 저장된 내용을 다른 곳에서 보여줄 필요가 없다면 이 포맷을 사용하기를 권장합니다.ver:0x0505010B
            "HWPML2X": HWP 형식과 호환. 문서의 모든 정보를 유지
            "HTML": 인터넷 문서 HTML 형식. 한/글 고유의 서식은 손실된다.
            "UNICODE": 유니코드 텍스트, 서식정보가 없는 텍스트만 저장.
            "TEXT": 일반 텍스트. 유니코드에만 있는 정보(한자, 고어, 특수문자 등)는 모두 손실된다.
            소문자로 입력해도 된다.

        :param option:
            "saveblock": 선택된 블록만 저장. 개체 선택 상태에서는 동작하지 않는다.
            기본값은 빈 문자열("")

        :return:
            지정된 포맷에 맞춰 파일을 문자열로 변환한 값을 반환한다.

        Examples:
            >>> self.hwp.get_text_file()
            'ㅁㄴㅇㄹ\r\nㅁㄴㅇㄹ\r\nㅁㄴㅇㄹ\r\n\r\nㅂㅈㄷㄱ\r\nㅂㅈㄷㄱ\r\nㅂㅈㄷㄱ\r\n'
        """
        return self.hwp.GetTextFile(Format=format, option=option)

    def get_translate_lang_list(self, cur_lang):
        return self.hwp.GetTranslateLangList(curLang=cur_lang)

    def get_user_info(self, user_info_id):
        return self.hwp.GetUserInfo(userInfoId=user_info_id)

    def gradation(self, gradation):
        return self.hwp.Gradation(Gradation=gradation)

    def grid_method(self, grid_method):
        return self.hwp.GridMethod(GridMethod=grid_method)

    def grid_view_line(self, grid_view_line):
        return self.hwp.GridViewLine(GridViewLine=grid_view_line)

    def gutter_method(self, gutter_type):
        return self.hwp.GutterMethod(GutterType=gutter_type)

    def h_align(self, h_align):
        return self.hwp.HAlign(HAlign=h_align)

    def handler(self, handler):
        return self.hwp.Handler(Handler=handler)

    def hash(self, hash):
        return self.hwp.Hash(Hash=hash)

    def hatch_style(self, hatch_style):
        return self.hwp.HatchStyle(HatchStyle=hatch_style)

    def head_type(self, heading_type):
        return self.hwp.HeadType(HeadingType=heading_type)

    def height_rel(self, height_rel):
        return self.hwp.HeightRel(HeightRel=height_rel)

    def hiding(self, hiding):
        return self.hwp.Hiding(Hiding=hiding)

    def horz_rel(self, horz_rel):
        return self.hwp.HorzRel(HorzRel=horz_rel)

    def hwp_line_type(self, line_type):
        return self.hwp.HwpLineType(LineType=line_type)

    def hwp_line_width(self, line_width):
        return self.hwp.HwpLineWidth(LineWidth=line_width)

    def hwp_outline_style(self, hwp_outline_style):
        return self.hwp.HwpOutlineStyle(HwpOutlineStyle=hwp_outline_style)

    def hwp_outline_type(self, hwp_outline_type):
        return self.hwp.HwpOutlineType(HwpOutlineType=hwp_outline_type)

    def hwp_underline_shape(self, hwp_underline_shape):
        return self.hwp.HwpUnderlineShape(HwpUnderlineShape=hwp_underline_shape)

    def hwp_underline_type(self, hwp_underline_type):
        return self.hwp.HwpUnderlineType(HwpUnderlineType=hwp_underline_type)

    def hwp_zoom_type(self, zoom_type):
        return self.hwp.HwpZoomType(ZoomType=zoom_type)

    def image_format(self, image_format):
        return self.hwp.ImageFormat(ImageFormat=image_format)

    def import_style(self, sty_filepath):
        """
        미리 저장된 특정 sty파일의 스타일을 임포트한다.

        :param sty_filepath:
            sty파일의 경로

        :return:
            성공시 True, 실패시 False

        :Examples
            >>> self.hwp.import_style("C:/Users/User/Desktop/new_style.sty")
            True
        """
        style_set = self.hwp.HParameterSet.HStyleTemplate
        style_set.filename = sty_filepath
        return self.hwp.ImportStyle(style_set.HSet)

    def init_hparameter_set(self):
        return self.hwp.InitHParameterSet()

    def init_scan(self, option=0x07, range=0x77, spara=0, spos=0, epara=-1, epos=-1):
        """
        문서의 내용을 검색하기 위해 초기설정을 한다.
        문서의 검색 과정은 InitScan()으로 검색위한 준비 작업을 하고
        GetText()를 호출하여 본문의 텍스트를 얻어온다.
        GetText()를 반복호출하면 연속하여 본문의 텍스트를 얻어올 수 있다.
        검색이 끝나면 ReleaseScan()을 호출하여 관련 정보를 Release해야 한다.

        :param option:
            찾을 대상을 다음과 같은 옵션을 조합하여 지정할 수 있다.
            생략하면 모든 컨트롤을 찾을 대상으로 한다.
            0x00: 본문을 대상으로 검색한다.(서브리스트를 검색하지 않는다.) - maskNormal
            0x01: char 타입 컨트롤 마스크를 대상으로 한다.(강제줄나눔, 문단 끝, 하이픈, 묶움빈칸, 고정폭빈칸, 등...) - maskChar
            0x02: inline 타입 컨트롤 마스크를 대상으로 한다.(누름틀 필드 끝, 등...) - maskInline
            0x04: extende 타입 컨트롤 마스크를 대상으로 한다.(바탕쪽, 프레젠테이션, 다단, 누름틀 필드 시작, Shape Object, 머리말, 꼬리말, 각주, 미주, 번호관련 컨트롤, 새 번호 관련 컨트롤, 감추기, 찾아보기, 글자 겹침, 등...) - maskCtrl

        :param range:
            검색의 범위를 다음과 같은 옵션을 조합(sum)하여 지정할 수 있다.
            생략하면 "문서 시작부터 - 문서의 끝까지" 검색 범위가 지정된다.
            0x0000: 캐럿 위치부터. (시작 위치) - scanSposCurrent
            0x0010: 특정 위치부터. (시작 위치) - scanSposSpecified
            0x0020: 줄의 시작부터. (시작 위치) - scanSposLine
            0x0030: 문단의 시작부터. (시작 위치) - scanSposParagraph
            0x0040: 구역의 시작부터. (시작 위치) - scanSposSection
            0x0050: 리스트의 시작부터. (시작 위치) - scanSposList
            0x0060: 컨트롤의 시작부터. (시작 위치) - scanSposControl
            0x0070: 문서의 시작부터. (시작 위치) - scanSposDocument
            0x0000: 캐럿 위치까지. (끝 위치) - scanEposCurrent
            0x0001: 특정 위치까지. (끝 위치) - scanEposSpecified
            0x0002: 줄의 끝까지. (끝 위치) - scanEposLine
            0x0003: 문단의 끝까지. (끝 위치) - scanEposParagraph
            0x0004: 구역의 끝까지. (끝 위치) - scanEposSection
            0x0005: 리스트의 끝까지. (끝 위치) - scanEposList
            0x0006: 컨트롤의 끝까지. (끝 위치) - scanEposControl
            0x0007: 문서의 끝까지. (끝 위치) - scanEposDocument
            0x00ff: 검색의 범위를 블록으로 제한. - scanWithinSelection
            0x0000: 정뱡향. (검색 방향) - scanForward
            0x0100: 역방향. (검색 방향) - scanBackward

        :param spara:
            검색 시작 위치의 문단 번호.
            scanSposSpecified 옵션이 지정되었을 때만 유효하다.
            예) range=0x0011

        :param spos:
            검색 시작 위치의 문단 중에서 문자의 위치.
            scanSposSpecified 옵션이 지정되었을 때만 유효하다.
            예) range=0x0011

        :param epara:
            검색 끝 위치의 문단 번호.
            scanEposSpecified 옵션이 지정되었을 때만 유효하다.

        :param epos:
            검색 끝 위치의 문단 중에서 문자의 위치.
            scanEposSpecified 옵션이 지정되었을 때만 유효하다.

        :return:
            성공하면 True, 실패하면 False

        Examples:
            >>> self.hwp.init_scan(range=0xff)
            >>> _, text = self.hwp.get_text()
            >>> self.hwp.release_scan()
            >>> print(text)
            Hello, world!
        """
        return self.hwp.InitScan(option=option, Range=range, spara=spara,
                             spos=spos, epara=epara, epos=epos)

    def insert(self, path, format="", arg=""):
        """
        현재 캐럿 위치에 문서파일을 삽입한다.
        format, arg에 대해서는 self.hwp.open 참조

        :param path:
            문서파일의 경로

        :param format:
            문서형식. **빈 문자열을 지정하면 자동으로 선택한다.**
            생략하면 빈 문자열이 지정된다.
            아래에 쓰여 있는 대로 대문자로만 써야 한다.
            "HWPX": 한/글 hwpx format
            "HWP": 한/글 native format
            "HWP30": 한/글 3.X/96/97
            "HTML": 인터넷 문서
            "TEXT": 아스키 텍스트 문서
            "UNICODE": 유니코드 텍스트 문서
            "HWP20": 한글 2.0
            "HWP21": 한글 2.1/2.5
            "HWP15": 한글 1.X
            "HWPML1X": HWPML 1.X 문서 (Open만 가능)
            "HWPML2X": HWPML 2.X 문서 (Open / SaveAs 가능)
            "RTF": 서식 있는 텍스트 문서
            "DBF": DBASE II/III 문서
            "HUNMIN": 훈민정음 3.0/2000
            "MSWORD": 마이크로소프트 워드 문서
            "DOCRTF": MS 워드 문서 (doc)
            "OOXML": MS 워드 문서 (docx)
            "HANA": 하나워드 문서
            "ARIRANG": 아리랑 문서
            "ICHITARO": 一太郞 문서 (일본 워드프로세서)
            "WPS": WPS 문서
            "DOCIMG": 인터넷 프레젠테이션 문서(SaveAs만 가능)
            "SWF": Macromedia Flash 문서(SaveAs만 가능)

        :param arg:
            세부옵션. 의미는 format에 지정한 파일형식에 따라 다르다.
            조합 가능하며, 생략하면 빈 문자열이 지정된다.
            <공통>
            "setcurdir:FALSE;" :로드한 후 해당 파일이 존재하는 폴더로 현재 위치를 변경한다. hyperlink 정보가 상대적인 위치로 되어 있을 때 유용하다.
            <HWP/HWPX>
            "lock:TRUE;": 로드한 후 해당 파일을 계속 오픈한 상태로 lock을 걸지 여부
            "notext:FALSE;": 텍스트 내용을 읽지 않고 헤더 정보만 읽을지 여부. (스타일 로드 등에 사용)
            "template:FALSE;": 새로운 문서를 생성하기 위해 템플릿 파일을 오픈한다. 이 옵션이 주어지면 lock은 무조건 FALSE로 처리된다.
            "suspendpassword:FALSE;": TRUE로 지정하면 암호가 있는 파일일 경우 암호를 묻지 않고 무조건 읽기에 실패한 것으로 처리한다.
            "forceopen:FALSE;": TRUE로 지정하면 읽기 전용으로 읽어야 하는 경우 대화상자를 띄우지 않는다.
            "versionwarning:FALSE;": TRUE로 지정하면 문서가 상위버전일 경우 메시지 박스를 띄우게 된다.
            <HTML>
            "code"(string, codepage): 문서변환 시 사용되는 코드 페이지를 지정할 수 있으며 code키가 존재할 경우 필터사용 시 사용자 다이얼로그를  띄우지 않는다.
            (코드페이지 종류는 아래와 같다.)
            ("utf8" : UTF8)
            ("unicode": 유니코드)
            ("ks":  한글 KS 완성형)
            ("acp" : Active Codepage 현재 시스템의 코드 페이지)
            ("kssm": 한글 조합형)
            ("sjis" : 일본)
            ("gb" : 중국 간체)
            ("big5" : 중국 번체)
            "textunit:(string, pixel);": Export될 Text의 크기의 단위 결정.pixel, point, mili 지정 가능.
            "formatunit:(string, pixel);": Export될 문서 포맷 관련 (마진, Object 크기 등) 단위 결정. pixel, point, mili 지정 가능
            <DOCIMG>
            "asimg:FALSE;": 저장할 때 페이지를 image로 저장
            "ashtml:FALSE;": 저장할 때 페이지를 html로 저장
            <TEXT>
            "code:(string, codepage);": 문서 변환 시 사용되는 코드 페이지를 지정할 수 있으며
            code키가 존재할 경우 필터 사용 시 사용자 다이얼로그를  띄우지 않는다.

        :return:
            성공하면 True, 실패하면 False
        """
        return self.hwp.Insert(Path=path, Format=format, arg=arg)

    def insert_background_picture(self, path, border_type="SelectedCell",
                                  embedded=True, filloption=5, effect=1,
                                  watermark=False, brightness=0, contrast=0) -> bool:
        """
        **셀**에 배경이미지를 삽입한다.
        CellBorderFill의 SetItem 중 FillAttr 의 SetItem FileName 에
        이미지의 binary data를 지정해 줄 수가 없어서 만든 함수다.
        기타 배경에 대한 다른 조정은 Action과 ParameterSet의 조합으로 가능하다.

        :param path:
            삽입할 이미지 파일

        :param border_type:
            배경 유형을 문자열로 지정(파라미터 이름과는 다르게 삽입/제거 기능이다.)
            "SelectedCell": 현재 선택된 표의 셀의 배경을 변경한다.
            "SelectedCellDelete": 현재 선택된 표의 셀의 배경을 지운다.
            단, 배경 제거시 반드시 셀이 선택되어 있어야함.
            커서가 위치하는 것만으로는 동작하지 않음.

        :param embedded:
            이미지 파일을 문서 내에 포함할지 여부 (True/False). 생략하면 True

        :param filloption:
            삽입할 그림의 크기를 지정하는 옵션
            0: 바둑판식으로 - 모두
            1: 바둑판식으로 - 가로/위
            2: 바둑판식으로 - 가로/아로
            3: 바둑판식으로 - 세로/왼쪽
            4: 바둑판식으로 - 세로/오른쪽
            5: 크기에 맞추어(기본값)
            6: 가운데로
            7: 가운데 위로
            8: 가운데 아래로
            9: 왼쪽 가운데로
            10: 왼쪽 위로
            11: 왼쪽 아래로
            12: 오른쪽 가운데로
            13: 오른쪽 위로
            14: 오른쪽 아래로

        :param effect:
            이미지효과
            0: 원래 그림(기본값)
            1: 그레이 스케일
            2: 흑백으로

        :param watermark:
            watermark효과 유무 (True/False)
            기본값은 False
            이 옵션이 True이면 brightness 와 contrast 옵션이 무시된다.

        :param brightness:
            밝기 지정(-100 ~ 100), 기본 값은 0

        :param contrast:
            선명도 지정(-100 ~ 100), 기본 값은 0

        :return:
            성공했을 경우 True, 실패했을 경우 False

        Examples:
            >>> self.hwp.insert_background_picture(path="C:/Users/User/Desktop/KakaoTalk_20230709_023118549.jpg")
            True
        """
        return self.hwp.InsertBackgroundPicture(Path=path, BorderType=border_type,
                                            Embedded=embedded, filloption=filloption,
                                            Effect=effect, watermark=watermark,
                                            Brightness=brightness, Contrast=contrast)

    def insert_ctrl(self, ctrl_id, initparam):
        """
        현재 캐럿 위치에 컨트롤을 삽입한다.
        ctrlid에 지정할 수 있는 컨트롤 ID는 HwpCtrl.CtrlID가 반환하는 ID와 동일하다.
        자세한 것은  Ctrl 오브젝트 Properties인 CtrlID를 참조.
        initparam에는 컨트롤의 초기 속성을 지정한다.
        대부분의 컨트롤은 Ctrl.Properties와 동일한 포맷의 parameter set을 사용하지만,
        컨트롤 생성 시에는 다른 포맷을 사용하는 경우도 있다.
        예를 들어 표의 경우 Ctrl.Properties에는 "Table" 셋을 사용하지만,
        생성 시 initparam에 지정하는 값은 "TableCreation" 셋이다.

        :param ctrl_id:
            삽입할 컨트롤 ID

        :param initparam:
            컨트롤 초기속성. 생략하면 default 속성으로 생성한다.

        :return:
            생성된 컨트롤 object

        Examples:
            >>> # 3행5열의 표를 삽입한다.
            >>> from time import sleep
            >>> tbset = self.hwp.CreateSet("TableCreation")
            >>> tbset.SetItem("Rows", 3)
            >>> tbset.SetItem("Cols", 5)
            >>> row_set = tbset.CreateItemArray("RowHeight", 3)
            >>> col_set = tbset.CreateItemArray("ColWidth", 5)
            >>> row_set.SetItem(0, self.hwp.PointToHwpUnit(10))
            >>> row_set.SetItem(1, self.hwp.PointToHwpUnit(10))
            >>> row_set.SetItem(2, self.hwp.PointToHwpUnit(10))
            >>> col_set.SetItem(0, self.hwp.MiliToHwpUnit(26))
            >>> col_set.SetItem(1, self.hwp.MiliToHwpUnit(26))
            >>> col_set.SetItem(2, self.hwp.MiliToHwpUnit(26))
            >>> col_set.SetItem(3, self.hwp.MiliToHwpUnit(26))
            >>> col_set.SetItem(4, self.hwp.MiliToHwpUnit(26))
            >>> table = self.hwp.InsertCtrl("tbl", tbset)
            >>> sleep(3)  # 표 생성 3초 후 다시 표 삭제
            >>> self.hwp.delete_ctrl(table)


        """
        return self.hwp.InsertCtrl(CtrlID=ctrl_id, initparam=initparam)

    def insert_picture(self, path, embedded=True, sizeoption=2, reverse=False, watermark=False, effect=0, width=0,
                       height=0):
        """
        현재 캐럿의 위치에 그림을 삽입한다.
        다만, 그림의 종횡비를 유지한 채로 셀의 높이만 키워주는 옵션이 없다.
        이런 작업을 원하는 경우에는 그림을 클립보드로 복사하고,
        Ctrl-V로 붙여넣기를 하는 수 밖에 없다.
        또한, 셀의 크기를 조절할 때 이미지의 크기도 따라 변경되게 하고 싶다면
        insert_background_picture 함수를 사용하는 것도 좋다.

        :param path:
            삽입할 이미지 파일의 전체경로

        :param embedded:
            이미지 파일을 문서 내에 포함할지 여부 (True/False). 생략하면 True

        :param sizeoption:
            삽입할 그림의 크기를 지정하는 옵션. 기본값은 2
            0: 이미지 원래의 크기로 삽입한다. width와 height를 지정할 필요 없다.(realSize)
            1: width와 height에 지정한 크기로 그림을 삽입한다.(specificSize)
            2: 현재 캐럿이 표의 셀 안에 있을 경우, 셀의 크기에 맞게 자동 조절하여 삽입한다. (종횡비 유지안함)(cellSize)
               캐럿이 셀 안에 있지 않으면 이미지의 원래 크기대로 삽입된다.
            3: 현재 캐럿이 표의 셀 안에 있을 경우, 셀의 크기에 맞추어 원본 이미지의 가로 세로의 비율이 동일하게 확대/축소하여 삽입한다.(cellSizeWithSameRatio)

        :param reverse: 이미지의 반전 유무 (True/False). 기본값은 False

        :param watermark: watermark효과 유무 (True/False). 기본값은 False

        :param effect:
            그림 효과
            0: 실제 이미지 그대로
            1: 그레이 스케일
            2: 흑백효과

        :param width:
            그림의 가로 크기 지정. 단위는 mm(HWPUNIT 아님!)

        :param height:
            그림의 높이 크기 지정. 단위는 mm

        :return:
            생성된 컨트롤 object.

        Examples:
            >>> ctrl = self.hwp.insert_picture("C:/Users/Administrator/Desktop/KakaoTalk_20230709_023118549.jpg")
            >>> pset = ctrl.Properties  # == self.hwp.create_set("ShapeObject")
            >>> pset.SetItem("TreatAsChar", False)  # 글자처럼취급 해제
            >>> pset.SetItem("TextWrap", 2)  # 그림을 글 뒤로
            >>> ctrl.Properties = pset  # 설정한 값 적용(간단!)
        """
        return self.hwp.InsertPicture(Path=path, Embedded=embedded, sizeoption=sizeoption,
                                  Reverse=reverse, watermark=watermark, Effect=effect,
                                  Width=width, Height=height)

    def is_action_enable(self, action_id):
        return self.hwp.IsActionEnable(actionID=action_id)

    def is_command_lock(self, action_id):
        """
        해당 액션이 잠겨있는지 확인한다.

        :param action_id: 액션 ID. (ActionIDTable.Hwp 참조)

        :return:
            잠겨있으면 True, 잠겨있지 않으면 False를 반환한다.
        """
        return self.hwp.IsCommandLock(actionID=action_id)

    def key_indicator(self) -> tuple:
        """
        상태 바의 정보를 얻어온다.
        (캐럿이 표 안에 있을 때 셀의 주소를 얻어오는 거의 유일한 방법이다.)

        :return:
            튜플(succ, seccnt, secno, prnpageno, colno, line, pos, over, ctrlname)
            succ: 성공하면 True, 실패하면 False (항상 True임..)
            seccnt: 총 구역
            secno: 현재 구역
            prnpageno: 쪽
            colno: 단
            line: 줄
            pos: 칸
            over: 삽입모드 (True: 수정, False: 삽입)
            ctrlname: 캐럿이 위치한 곳의 컨트롤이름

        Examples:
            >>> # 현재 셀 주소(표 안에 있을 때)
            >>> self.hwp.KeyIndicator()[-1][1:].split(")")[0]
            "A1"
        """
        return self.hwp.KeyIndicator()

    def line_spacing_method(self, line_spacing):
        return self.hwp.LineSpacingMethod(LineSpacing=line_spacing)

    def line_wrap_type(self, line_wrap):
        return self.hwp.LineWrapType(LineWrap=line_wrap)

    def lock_command(self, act_id, is_lock):
        """
        특정 액션이 실행되지 않도록 잠근다.

        :param act_id: 액션 ID. (ActionIDTable.Hwp 참조)

        :param is_lock:
            True이면 액션의 실행을 잠그고, False이면 액션이 실행되도록 한다.

        :return: None

        Examples:
            >>> # Undo와 Redo 잠그기
            >>> self.hwp.LockCommand("Undo", True)
            >>> self.hwp.LockCommand("Redo", True)
        """
        return self.hwp.LockCommand(ActID=act_id, isLock=is_lock)

    def lunar_to_solar(self, l_year, l_month, l_day, l_leap, s_year, s_month, s_day):
        return self.hwp.LunarToSolar(lYear=l_year, lMonth=l_month, lDay=l_day, lLeap=l_leap,
                                 sYear=s_year, sMonth=s_month, sDay=s_day)

    def lunar_to_solar_by_set(self, l_year, l_month, l_day, l_leap):
        return self.hwp.LunarToSolarBySet(lYear=l_year, lMonth=l_month, lLeap=l_leap)

    def macro_state(self, macro_state):
        return self.hwp.MacroState(MacroState=macro_state)

    def mail_type(self, mail_type):
        return self.hwp.MailType(MailType=mail_type)

    def metatag_exist(self, tag):
        return self.hwp.MetatagExist(tag=tag)

    def mili_to_hwp_unit(self, mili):
        return self.hwp.MiliToHwpUnit(mili=mili)

    def modify_field_properties(self, field, remove, add):
        """
        지정한 필드의 속성을 바꾼다.
        양식모드에서 편집가능/불가 여부를 변경하는 메서드지만,
        현재 양식모드에서 어떤 속성이라도 편집가능하다..
        혹시 필드명이나 메모, 지시문을 수정하고 싶다면
        set_cur_field_name 메서드를 사용하자.

        :param field:
        :param remove:
        :param add:
        :return:
        """
        return self.hwp.ModifyFieldProperties(Field=field, remove=remove, Add=add)

    def modify_metatag_properties(self, tag, remove, add):
        return self.hwp.ModifyMetatagProperties(tag=tag, remove=remove, Add=add)

    def move_pos(self, move_id=1, para=0, pos=0):
        """
        캐럿의 위치를 옮긴다.
        move_id를 200(moveScrPos)으로 지정한 경우에는
        스크린 좌표로 마우스 커서의 (x,y)좌표를 그대로 넘겨주면 된다.
        201(moveScanPos)는 문서를 검색하는 중 캐럿을 이동시키려 할 경우에만 사용이 가능하다.
        (솔직히 200 사용법은 잘 모르겠다;)

        :param move_id:
            아래와 같은 값을 지정할 수 있다. 생략하면 1(moveCurList)이 지정된다.
            0: 루트 리스트의 특정 위치.(para pos로 위치 지정) moveMain
            1: 현재 리스트의 특정 위치.(para pos로 위치 지정) moveCurList
            2: 문서의 시작으로 이동. moveTopOfFile
            3: 문서의 끝으로 이동. moveBottomOfFile
            4: 현재 리스트의 시작으로 이동 moveTopOfList
            5: 현재 리스트의 끝으로 이동 moveBottomOfList
            6: 현재 위치한 문단의 시작으로 이동 moveStartOfPara
            7: 현재 위치한 문단의 끝으로 이동 moveEndOfPara
            8: 현재 위치한 단어의 시작으로 이동.(현재 리스트만을 대상으로 동작한다.) moveStartOfWord
            9: 현재 위치한 단어의 끝으로 이동.(현재 리스트만을 대상으로 동작한다.) moveEndOfWord
            10: 다음 문단의 시작으로 이동.(현재 리스트만을 대상으로 동작한다.) moveNextPara
            11: 앞 문단의 끝으로 이동.(현재 리스트만을 대상으로 동작한다.) movePrevPara
            12: 한 글자 뒤로 이동.(서브 리스트를 옮겨 다닐 수 있다.) moveNextPos
            13: 한 글자 앞으로 이동.(서브 리스트를 옮겨 다닐 수 있다.) movePrevPos
            14: 한 글자 뒤로 이동.(서브 리스트를 옮겨 다닐 수 있다. 머리말/꼬리말, 각주/미주, 글상자 포함.) moveNextPosEx
            15: 한 글자 앞으로 이동.(서브 리스트를 옮겨 다닐 수 있다. 머리말/꼬리말, 각주/미주, 글상자 포함.) movePrevPosEx
            16: 한 글자 뒤로 이동.(현재 리스트만을 대상으로 동작한다.) moveNextChar
            17: 한 글자 앞으로 이동.(현재 리스트만을 대상으로 동작한다.) movePrevChar
            18: 한 단어 뒤로 이동.(현재 리스트만을 대상으로 동작한다.) moveNextWord
            19: 한 단어 앞으로 이동.(현재 리스트만을 대상으로 동작한다.) movePrevWord
            20: 한 줄 아래로 이동. moveNextLine
            21: 한 줄 위로 이동. movePrevLine
            22: 현재 위치한 줄의 시작으로 이동. moveStartOfLine
            23: 현재 위치한 줄의 끝으로 이동. moveEndOfLine
            24: 한 레벨 상위로 이동한다. moveParentList
            25: 탑레벨 리스트로 이동한다. moveTopLevelList
            26: 루트 리스트로 이동한다. 현재 루트 리스트에 위치해 있어 더 이상 상위 리스트가 없을 때는 위치 이동 없이 반환한다. 이동한 후의 위치는 상위 리스트에서 서브리스트가 속한 컨트롤 코드가 위치한 곳이다. 위치 이동시 셀렉션은 무조건 풀린다. moveRootList
            27: 현재 캐럿이 위치한 곳으로 이동한다. (캐럿 위치가 뷰의 맨 위쪽으로 올라간다.) moveCurrentCaret
            100: 현재 캐럿이 위치한 셀의 왼쪽 moveLeftOfCell
            101: 현재 캐럿이 위치한 셀의 오른쪽 moveRightOfCell
            102: 현재 캐럿이 위치한 셀의 위쪽 moveUpOfCell
            103: 현재 캐럿이 위치한 셀의 아래쪽 moveDownOfCell
            104: 현재 캐럿이 위치한 셀에서 행(row)의 시작 moveStartOfCell
            105: 현재 캐럿이 위치한 셀에서 행(row)의 끝 moveEndOfCell
            106: 현재 캐럿이 위치한 셀에서 열(column)의 시작 moveTopOfCell
            107: 현재 캐럿이 위치한 셀에서 열(column)의 끝 moveBottomOfCell
            200: 한/글 문서창에서의 screen 좌표로서 위치를 설정 한다. moveScrPos
            201: GetText() 실행 후 위치로 이동한다. moveScanPos

        :param para:
            이동할 문단의 번호.
            0(moveMain) 또는 1(moveCurList)가 지정되었을 때만 사용된다.
            200(moveScrPos)가 지정되었을 때는 문단번호가 아닌 스크린 좌표로 해석된다.
            (스크린 좌표 : LOWORD = x좌표, HIWORD = y좌표)

        :param pos:
            이동할 문단 중에서 문자의 위치.
            0(moveMain) 또는 1(moveCurList)가 지정되었을 때만 사용된다.

        :return:
            성공하면 True, 실패하면 False
        """
        return self.hwp.MovePos(moveID=move_id, Para=para, Pos=pos)

    def move_to_field(self, field, text=True, start=True, select=False):
        """
        지정한 필드로 캐럿을 이동한다.

        :param field:
            필드이름. GetFieldText()/PutFieldText()와 같은 형식으로
            이름 뒤에 ‘{{#}}’로 번호를 지정할 수 있다.

        :param text:
            필드가 누름틀일 경우 누름틀 내부의 텍스트로 이동할지(True)
            누름틀 코드로 이동할지(False)를 지정한다.
            누름틀이 아닌 필드일 경우 무시된다. 생략하면 True가 지정된다.

        :param start:
            필드의 처음(True)으로 이동할지 끝(False)으로 이동할지 지정한다.
            select를 True로 지정하면 무시된다. 생략하면 True가 지정된다.

        :param select:
            필드 내용을 블록으로 선택할지(True), 캐럿만 이동할지(False) 지정한다.
            생략하면 False가 지정된다.
        :return:
        """
        return self.hwp.MoveToField(Field=field, Text=text, start=start, Select=select)

    def move_to_metatag(self, tag, text, start, select):
        return self.hwp.MoveToMetatag(tag=tag, Text=text, start=start, select=select)

    def number_format(self, num_format):
        return self.hwp.NumberFormat(NumFormat=num_format)

    def numbering(self, numbering):
        return self.hwp.Numbering(Numbering=numbering)

    def open(self, filename, format="", arg=""):
        """
        문서를 연다.

        :param filename:
            문서 파일의 전체경로

        :param format:
            문서 형식. 빈 문자열을 지정하면 자동으로 인식한다. 생략하면 빈 문자열이 지정된다.
            "HWP": 한/글 native format
            "HWP30": 한/글 3.X/96/97
            "HTML": 인터넷 문서
            "TEXT": 아스키 텍스트 문서
            "UNICODE": 유니코드 텍스트 문서
            "HWP20": 한글 2.0
            "HWP21": 한글 2.1/2.5
            "HWP15": 한글 1.X
            "HWPML1X": HWPML 1.X 문서 (Open만 가능)
            "HWPML2X": HWPML 2.X 문서 (Open / SaveAs 가능)
            "RTF": 서식 있는 텍스트 문서
            "DBF": DBASE II/III 문서
            "HUNMIN": 훈민정음 3.0/2000
            "MSWORD": 마이크로소프트 워드 문서
            "DOCRTF": MS 워드 문서 (doc)
            "OOXML": MS 워드 문서 (docx)
            "HANA": 하나워드 문서
            "ARIRANG": 아리랑 문서
            "ICHITARO": 一太郞 문서 (일본 워드프로세서)
            "WPS": WPS 문서
            "DOCIMG": 인터넷 프레젠테이션 문서(SaveAs만 가능)
            "SWF": Macromedia Flash 문서(SaveAs만 가능)

        :param arg:
            세부 옵션. 의미는 format에 지정한 파일 형식에 따라 다르다. 생략하면 빈 문자열이 지정된다.
            arg에 지정할 수 있는 옵션의 의미는 필터가 정의하기에 따라 다르지만,
            syntax는 다음과 같이 공통된 형식을 사용한다.
            "key:value;key:value;..."
            * key는 A-Z, a-z, 0-9, _ 로 구성된다.
            * value는 타입에 따라 다음과 같은 3 종류가 있다.
	        boolean: ex) fullsave:true (== fullsave)
	        integer: ex) type:20
	        string:  ex) prefix:_This_
            * value는 생략 가능하며, 이때는 콜론도 생략한다.
            * arg에 지정할 수 있는 옵션
            <모든 파일포맷>
                - setcurdir(boolean, true/false)
                    로드한 후 해당 파일이 존재하는 폴더로 현재 위치를 변경한다.
                    hyperlink 정보가 상대적인 위치로 되어 있을 때 유용하다.
            <HWP(HWPX)>
                - lock (boolean, TRUE)
                    로드한 후 해당 파일을 계속 오픈한 상태로 lock을 걸지 여부
                - notext (boolean, FALSE)
                    텍스트 내용을 읽지 않고 헤더 정보만 읽을지 여부. (스타일 로드 등에 사용)
                - template (boolean, FALSE)
                    새로운 문서를 생성하기 위해 템플릿 파일을 오픈한다.
                    이 옵션이 주어지면 lock은 무조건 FALSE로 처리된다.
                - suspendpassword (boolean, FALSE)
                    TRUE로 지정하면 암호가 있는 파일일 경우 암호를 묻지 않고 무조건 읽기에 실패한 것으로 처리한다.
                - forceopen (boolean, FALSE)
                    TRUE로 지정하면 읽기 전용으로 읽어야 하는 경우 대화상자를 띄우지 않는다.
                - versionwarning (boolean, FALSE)
                    TRUE로 지정하면 문서가 상위버전일 경우 메시지 박스를 띄우게 된다.
            <HTML>
                - code(string, codepage)
                    문서변환 시 사용되는 코드 페이지를 지정할 수 있으며 code키가 존재할 경우 필터사용 시 사용자 다이얼로그를  띄우지 않는다.
                - textunit(boolean, pixel)
                    Export될 Text의 크기의 단위 결정.pixel, point, mili 지정 가능.
                - formatunit(boolean, pixel)
                    Export될 문서 포맷 관련 (마진, Object 크기 등) 단위 결정. pixel, point, mili 지정 가능
                ※ [codepage 종류]
                    - ks :  한글 KS 완성형
                    - kssm: 한글 조합형
                    - sjis : 일본
                    - utf8 : UTF8
                    - unicode: 유니코드
                    - gb : 중국 간체
                    - big5 : 중국 번체
                    - acp : Active Codepage 현재 시스템의 코드 페이지
            <DOCIMG>
                - asimg(boolean, FALSE)
                    저장할 때 페이지를 image로 저장
                - ashtml(boolean, FALSE)
                    저장할 때 페이지를 html로 저장

        :return:
            성공하면 True, 실패하면 False
        """
        return self.hwp.Open(filename=filename, Format=format, arg=arg)

    def page_num_position(self, pagenumpos):
        return self.hwp.PageNumPosition(pagenumpos=pagenumpos)

    def page_type(self, page_type):
        return self.hwp.PageType(PageType=page_type)

    def para_head_align(self, para_head_align):
        return self.hwp.ParaHeadAlign(ParaHeadAlign=para_head_align)

    def pic_effect(self, pic_effect):
        return self.hwp.PicEffect(PicEffect=pic_effect)

    def placement_type(self, restart):
        return self.hwp.PlacementType(Restart=restart)

    def point_to_hwp_unit(self, point):
        return self.hwp.PointToHwpUnit(Point=point)

    def present_effect(self, prsnteffect):
        return self.hwp.PresentEffect(prsnteffect=prsnteffect)

    def print_device(self, print_device):
        return self.hwp.PrintDevice(PrintDevice=print_device)

    def print_paper(self, print_paper):
        return self.hwp.PrintPaper(PrintPaper=print_paper)

    def print_range(self, print_range):
        return self.hwp.PrintRange(PrintRange=print_range)

    def print_type(self, print_method):
        return self.hwp.PrintType(PrintMethod=print_method)

    def protect_private_info(self, protecting_char, private_pattern_type):
        """
        개인정보를 보호한다.
        한/글의 경우 “찾아서 보호”와 “선택 글자 보호”를 다른 기능으로 구현하였지만,
        API에서는 하나의 함수로 구현한다.

        :param potecting_char:
            보호문자. 개인정보는 해당문자로 가려진다.

        :param private_pattern_type:
            보호유형. 개인정보 유형마다 설정할 수 있는 값이 다르다.
            0값은 기본 보호유형으로 모든 개인정보를 보호문자로 보호한다.

        :return:
            개인정보를 보호문자로 치환한 경우에 true를 반환한다.
	        개인정보를 보호하지 못할 경우 false를 반환한다.
	        문자열이 선택되지 않은 상태이거나, 개체가 선택된 상태에서는 실패한다.
	        또한, 보호유형이 잘못된 설정된 경우에도 실패한다.
	        마지막으로 보호암호가 설정되지 않은 경우에도 실패하게 된다.
        """
        return self.hwp.ProtectPrivateInfo(PotectingChar=protecting_char, PrivatePatternType=private_pattern_type)

    def put_field_text(self, field, text):
        """
        지정한 필드의 내용을 채운다.
        현재 필드에 입력되어 있는 내용은 지워진다.
        채워진 내용의 글자모양은 필드에 지정해 놓은 글자모양을 따라간다.
        fieldlist의 필드 개수와, textlist의 텍스트 개수는 동일해야 한다.
        존재하지 않는 필드에 대해서는 무시한다.

        :param field:
            내용을 채울 필드 이름의 리스트.
            한 번에 여러 개의 필드를 지정할 수 있으며,
            형식은 GetFieldText와 동일하다.
            다만 필드 이름 뒤에 "{{#}}"로 번호를 지정하지 않으면
            해당 이름을 가진 모든 필드에 동일한 텍스트를 채워 넣는다.
            즉, PutFieldText에서는 ‘필드이름’과 ‘필드이름{{0}}’의 의미가 다르다.

        :param text:
            필드에 채워 넣을 문자열의 리스트.
            형식은 필드 리스트와 동일하게 필드의 개수만큼
            텍스트를 0x02로 구분하여 지정한다.

        :return: None

        Examples:
            >>> # 현재 캐럿 위치에 zxcv 필드 생성
            >>> self.hwp.create_field("zxcv")
            >>> # zxcv 필드에 "Hello world!" 텍스트 삽입
            >>> self.hwp.put_field_text("zxcv", "Hello world!")
        """
        return self.hwp.PutFieldText(Field=field, Text=text)

    def put_metatag_name_text(self, tag, text):
        return self.hwp.PutMetatagNameText(tag=tag, Text=text)

    def quit(self):
        """
        한/글을 종료한다.
        단, 저장되지 않은 변경사항이 있는 경우 팝업이 뜨므로
        clear나 save 등의 메서드를 실행한 후에 quit을 실행해야 한다.
        :return:
        """
        return self.hwp.Quit()

    def rgb_color(self, red, green, blue):
        return self.hwp.RGBColor(red=red, green=green, blue=blue)

    def register_module(self, module_type="FilePathCheckDLL", module_data="FilePathCheckerModule"):
        """
        (인스턴스 생성시 자동으로 실행된다.)
        한/글 컨트롤에 부가적인 모듈을 등록한다.
        사용자가 모르는 사이에 파일이 수정되거나 서버로 전송되는 것을 막기 위해
        한/글 오토메이션은 파일을 불러오거나 저장할 때 사용자로부터 승인을 받도록 되어있다.
        그러나 이미 검증받은 웹페이지이거나,
        이미 사용자의 파일 시스템에 대해 강력한 접근 권한을 갖는 응용프로그램의 경우에는
        이러한 승인절차가 아무런 의미가 없으며 오히려 불편하기만 하다.
        이런 경우 register_module을 통해 보안승인모듈을 등록하여 승인절차를 생략할 수 있다.

        :param module_type:
            모듈의 유형. 기본값은 "FilePathCheckDLL"이다.
            파일경로 승인모듈을 DLL 형태로 추가한다.

        :param module_data:
            Registry에 등록된 DLL 모듈 ID

        :return:
            추가모듈등록에 성공하면 True를, 실패하면 False를 반환한다.

        Examples:
            >>> # 사전에 레지스트리에 보안모듈이 등록되어 있어야 한다.
            >>> # 보다 자세한 설명은 공식문서 참조
            >>> self.hwp.register_module("FilePathChekDLL", "FilePathCheckerModule")
            True
        """
        self.register_regedit()
        return self.hwp.RegisterModule(ModuleType=module_type, ModuleData=module_data)

    def register_regedit(self):
        import os
        import subprocess
        from winreg import ConnectRegistry, HKEY_CURRENT_USER, OpenKey, KEY_WRITE, SetValueEx, REG_SZ, CloseKey

        location = [i.split(": ")[1] for i in subprocess.check_output(['pip', 'show', 'hwpx']).decode().split("\r\n") if
                    i.startswith("Location: ")][0]
        winup_path = r"Software\HNC\HwpAutomation\Modules"

        # HKEY_LOCAL_MACHINE와 연결 생성 후 핸들 얻음
        reg_handle = ConnectRegistry(None, HKEY_CURRENT_USER)

        # 얻은 행동을 사용해 WRITE 권한으로 레지스트리 키를 엶
        file_path_checker_module = winup_path + r"\FilePathCheckerModule"
        key = OpenKey(reg_handle, winup_path, 0, KEY_WRITE)
        SetValueEx(key, "FilePathCheckerModule", 0, REG_SZ, os.path.join(location, "FilePathCheckerModule.dll"))
        CloseKey(key)

    def register_private_info_pattern(self, private_type, private_pattern):
        """
        개인정보의 패턴을 등록한다.
        (현재 작동하지 않는다.)

        :param private_type:
            등록할 개인정보 유형. 다음의 값 중 하나다.
			0x0001: 전화번호
			0x0002: 주민등록번호
			0x0004: 외국인등록번호
			0x0008: 전자우편
			0x0010: 계좌번호
			0x0020: 신용카드번호
			0x0040: IP 주소
			0x0080: 생년월일
			0x0100: 주소
			0x0200: 사용자 정의

        :param private_pattern:
            등록할 개인정보 패턴. 예를 들면 이런 형태로 입력한다.
			(예) 주민등록번호 - "NNNNNN-NNNNNNN"
			한/글이 이미 정의한 패턴은 정의하면 안 된다.
			함수를 여러 번 호출하는 것을 피하기 위해 패턴을 “;”기호로 구분
			반속해서 입력할 수 있도록 한다.

        :return:
            등록이 성공하였으면 True, 실패하였으면 False

        Examples:
            >>> self.hwp.RegisterPrivateInfoPattern(0x01, "NNNN-NNNN;NN-NN-NNNN-NNNN")  # 전화번호패턴
        """
        return self.hwp.RegisterPrivateInfoPattern(PrivateType=private_type, PrivatePattern=private_pattern)

    def release_action(self, action):
        return self.hwp.ReleaseAction(action=action)

    def release_scan(self):
        """
        InitScan()으로 설정된 초기화 정보를 해제한다.
        텍스트 검색작업이 끝나면 반드시 호출하여 설정된 정보를 해제해야 한다.

        :return: None
        """
        return self.hwp.ReleaseScan()

    def rename_field(self, oldname, newname):
        """
        지정한 필드의 이름을 바꾼다.
        예를 들어 oldname에 "title{{0}}\x02title{{1}}",
        newname에 "tt1\x02tt2로 지정하면 첫 번째 title은 tt1로, 두 번째 title은 tt2로 변경된다.
        oldname의 필드 개수와, newname의 필드 개수는 동일해야 한다.
        존재하지 않는 필드에 대해서는 무시한다.

        :param oldname:
            이름을 바꿀 필드 이름의 리스트. 형식은 PutFieldText와 동일하게 "\x02"로 구분한다.

        :param newname:
            새로운 필드 이름의 리스트. oldname과 동일한 개수의 필드 이름을 "\x02"로 구분하여 지정한다.

        :return: None

        Examples:
            >>> self.hwp.create_field("asdf")  # "asdf" 필드 생성
            >>> self.hwp.rename_field("asdf", "zxcv")  # asdf 필드명을 "zxcv"로 변경
            >>> self.hwp.put_field_text("zxcv", "Hello world!")  # zxcv 필드에 텍스트 삽입
        """
        return self.hwp.RenameField(oldname=oldname, newname=newname)

    def rename_metatag(self, oldtag, newtag):
        return self.hwp.RenameMetatag(oldtag=oldtag, newtag=newtag)

    def replace_action(self, old_action_id, new_action_id):
        """
        특정 Action을 다른 Action으로 대체한다.
        이는 메뉴나 단축키로 호출되는 Action을 대체할 뿐,
        CreateAction()이나, Run() 등의 함수를 이용할 때에는 아무런 영향을 주지 않는다.
        즉, ReplaceAction(“Cut", "Copy")을 호출하여
        ”오려내기“ Action을 ”복사하기“ Action으로 교체하면
        Ctrl+X 단축키나 오려내기 메뉴/툴바 기능을 수행하더라도 복사하기 기능이 수행되지만,
        코드 상에서 Run("Cut")을 실행하면 오려내기 Action이 실행된다.
        또한, 대체된 Action을 원래의 Action으로 되돌리기 위해서는
        NewActionID의 값을 원래의 Action으로 설정한 뒤 호출한다. 이를테면 이런 식이다.
        >>> self.hwp.replace_action("Cut", "Cut")

        :param old_action_id:
            변경될 원본 Action ID.
            한/글 컨트롤에서 사용할 수 있는 Action ID는
            ActionTable.hwp(별도문서)를 참고한다.

        :param new_action_id:
            변경할 대체 Action ID.
            기존의 Action ID와 UserAction ID(ver:0x07050206) 모두 사용가능하다.

        :return:
            Action을 바꾸면 True를 바꾸지 못했다면 False를 반환한다.
        """

        return self.hwp.ReplaceAction(OldActionID=old_action_id, NewActionID=new_action_id)

    def replace_font(self, langid, des_font_name, des_font_type, new_font_name, new_font_type):
        return self.hwp.ReplaceFont(langid=langid, desFontName=des_font_name, desFontType=des_font_type,
                                    newFontName=new_font_name, newFontType=new_font_type)

    def revision(self, revision):
        return self.hwp.Revision(Revision=revision)

    def run(self, act_id):
        """
        액션을 실행한다. ActionTable.hwp 액션 리스트 중에서
        "별도의 파라미터가 필요하지 않은" 단순 액션을 run으로 호출할 수 있다.

        :param act_id:
            액션 ID (ActionIDTable.hwp 참조)

        :return:
            성공시 True, 실패시 False를 반환한다.
        """
        return self.hwp.HAction.Run(act_id)

    def run_script_macro(self, function_name, u_macro_type=0, u_script_type=0):
        """
        한/글 문서 내에 존재하는 매크로를 실행한다.
        문서매크로, 스크립트매크로 모두 실행 가능하다.
        재미있는 점은 한/글 내에서 문서매크로 실행시
        New, Open 두 개의 함수 밖에 선택할 수 없으므로
        별도의 함수를 정의하더라도 이 두 함수 중 하나에서 호출해야 하지만,
        (진입점이 되어야 함)
        self.hwp.run_script_macro 명령어를 통해서는 제한없이 실행할 수 있다.

        :param function_name:
            실행할 매크로 함수이름(전체이름)

        :param u_macro_type:
            매크로의 유형. 밑의 값 중 하나이다.
            0: 스크립트 매크로(전역 매크로-HWP_GLOBAL_MACRO_TYPE, 기본값)
            1: 문서 매크로(해당문서에만 저장/적용되는 매크로-HWP_DOCUMENT_MACRO_TYPE)

        :param u_script_type:
            스크립트의 유형. 현재는 javascript만을 유일하게 지원한다.
            아무 정수나 입력하면 된다. (기본값: 0)

        :return:
            무조건 True를 반환(매크로의 실행여부와 상관없음)

        Examples:
            >>> self.hwp.run_script_macro("OnDocument_New", u_macro_type=1)
            True
            >>> self.hwp.run_script_macro("OnScriptMacro_중국어1성")
            True
        """
        return self.hwp.RunScriptMacro(FunctionName=function_name, uMacroType=u_macro_type, uScriptType=u_script_type)

    def save(self, save_if_dirty=True):
        """
        현재 편집중인 문서를 저장한다.
        문서의 경로가 지정되어있지 않으면 “새 이름으로 저장” 대화상자가 뜬다.

        :param save_if_dirty:
            True를 지정하면 문서가 변경된 경우에만 저장한다.
            False를 지정하면 변경여부와 상관없이 무조건 저장한다.
            생략하면 True가 지정된다.

        :return:
            성공하면 True, 실패하면 False
        """
        return self.hwp.Save(save_if_dirty=save_if_dirty)

    def save_as(self, path, format="HWP", arg=""):
        """
        현재 편집중인 문서를 지정한 이름으로 저장한다.
        format, arg의 일반적인 개념에 대해서는 Open()참조.
        "Hwp" 포맷으로 파일 저장 시 arg에 지정할 수 있는 옵션은 다음과 같다.
        "lock:true" - 저장한 후 해당 파일을 계속 오픈한 상태로 lock을 걸지 여부
        "backup:false" - 백업 파일 생성 여부
        "compress:true" - 압축 여부
        "fullsave:false" - 스토리지 파일을 완전히 새로 생성하여 저장
        "prvimage:2" - 미리보기 이미지 (0=off, 1=BMP, 2=GIF)
        "prvtext:1" - 미리보기 텍스트 (0=off, 1=on)
        "autosave:false" - 자동저장 파일로 저장할 지 여부 (TRUE: 자동저장, FALSE: 지정 파일로 저장)
        "export" - 다른 이름으로 저장하지만 열린 문서는 바꾸지 않는다.(lock:false와 함께 설정되어 있을 시 동작)
        여러 개를 한꺼번에 할 경우에는 세미콜론으로 구분하여 연속적으로 사용할 수 있다.
        "lock:TRUE;backup:FALSE;prvtext:1"

        :param path:
            문서 파일의 전체경로

        :param format:
            문서 형식. 생략하면 "HWP"가 지정된다.

        :param arg:
            세부 옵션. 의미는 format에 지정한 파일 형식에 따라 다르다. 생략하면 빈 문자열이 지정된다.

        :return:
            성공하면 True, 실패하면 False
        """
        return self.hwp.SaveAs(Path=path, Format=format, arg=arg)

    def scan_font(self):
        return self.hwp.ScanFont()

    def select_text(self, spara, spos, epara, epos):
        """
        특정 범위의 텍스트를 블록선택한다.
        epos가 가리키는 문자는 포함되지 않는다.

        :param spara:
            블록 시작 위치의 문단 번호.

        :param spos:
            블록 시작 위치의 문단 중에서 문자의 위치.

        :param epara:
            블록 끝 위치의 문단 번호.

        :param epos:
            블록 끝 위치의 문단 중에서 문자의 위치.

        :return:
            성공하면 True, 실패하면 False
        """
        return self.hwp.SelectText(spara=spara, spos=spos, epara=epara, epos=epos)

    def set_bar_code_image(self, lp_image_path, pgno, index, x, y, width, height):
        """
        작동하지 않는다.

        :param lp_image_path:
        :param pgno:
        :param index:
        :param x:
        :param y:
        :param width:
        :param height:
        :return:
        """
        return self.hwp.SetBarCodeImage(lpImagePath=lp_image_path, pgno=pgno, index=index,
                                        X=x, Y=y, Width=width, Height=height)

    def set_cur_field_name(self, field, option, direction, memo):
        """
        현재 캐럿이 위치하는 곳의 필드이름을 설정한다.
        GetFieldList()의 옵션 중에 4(hwpFieldSelection) 옵션은 사용하지 않는다.

        :param field:
            데이터 필드 이름

        :param option:
            다음과 같은 옵션을 지정할 수 있다. 0을 지정하면 모두 off이다. 생략하면 0이 지정된다.
            1: 셀에 부여된 필드 리스트만을 구한다. hwpFieldClickHere와는 함께 지정할 수 없다.(hwpFieldCell)
            2: 누름틀에 부여된 필드 리스트만을 구한다. hwpFieldCell과는 함께 지정할 수 없다.(hwpFieldClickHere)

        :param direction:
            누름틀 필드의 안내문. 누름틀 필드일 때만 유효하다.

        :param memo:
            누름틀 필드의 메모. 누름틀 필드일 때만 유효하다.

        :return:
            성공하면 True, 실패하면 False
        """
        return self.hwp.SetCurFieldName(Field=field, option=option, Direction=direction, memo=memo)

    def set_cur_metatag_name(self, tag):
        return self.hwp.SetCurMetatagName(tag=tag)

    def set_drm_authority(self, authority):
        return self.hwp.SetDRMAuthority(authority=authority)

    def set_field_view_option(self, option):
        """
        양식모드와 읽기전용모드일 때 현재 열린 문서의 필드의 겉보기 속성(『』표시)을 바꾼다.
        EditMode와 비슷하게 현재 열려있는 문서에 대한 속성이다. 따라서 저장되지 않는다.
        (작동하지 않음)

        :param option:
            겉보기 속성 bit
            1: 누름틀의 『』을 표시하지 않음, 기타필드의 『』을 표시하지 않음
            2: 누름틀의 『』을 빨간색으로 표시, 기타필드의 『』을 흰색으로 표시(기본값)
            3: 누름틀의 『』을 흰색으로 표시, 기타필드의 『』을 흰색으로 표시

        :return:
            설정된 속성이 반환된다.
            에러일 경우 0이 반환된다.
        """
        return self.hwp.SetFieldViewOption(option=option)

    def set_message_box_mode(self, mode):
        """
        한/글에서 쓰는 다양한 메시지박스가 뜨지 않고,
        자동으로 특정 버튼을 클릭한 효과를 주기 위해 사용한다.
        한/글에서 한/글이 로드된 후 SetMessageBoxMode()를 호출해서 사용한다.
        SetMessageBoxMode는 하나의 파라메터를 받으며,
        해당 파라메터는 자동으로 스킵할 버튼의 값으로 설정된다.
        예를 들어, MB_OK_IDOK (0x00000001)값을 주면,
        MB_OK형태의 메시지박스에서 OK버튼이 눌린 효과를 낸다.

        :param mode:
            // 메시지 박스의 종류
            #define MB_MASK						0x00FFFFFF
            // 1. 확인(MB_OK) : IDOK(1)
            #define MB_OK_IDOK						0x00000001
            #define MB_OK_MASK						0x0000000F
            // 2. 확인/취소(MB_OKCANCEL) : IDOK(1), IDCANCEL(2)
            #define MB_OKCANCEL_IDOK					0x00000010
            #define MB_OKCANCEL_IDCANCEL				0x00000020
            #define MB_OKCANCEL_MASK					0x000000F0
            // 3. 종료/재시도/무시(MB_ABORTRETRYIGNORE) : IDABORT(3), IDRETRY(4), IDIGNORE(5)
            #define MB_ABORTRETRYIGNORE_IDABORT			0x00000100
            #define MB_ABORTRETRYIGNORE_IDRETRY			0x00000200
            #define MB_ABORTRETRYIGNORE_IDIGNORE			0x00000400
            #define MB_ABORTRETRYIGNORE_MASK				0x00000F00
            // 4. 예/아니오/취소(MB_YESNOCANCEL) : IDYES(6), IDNO(7), IDCANCEL(2)
            #define MB_YESNOCANCEL_IDYES				0x00001000
            #define MB_YESNOCANCEL_IDNO				0x00002000
            #define MB_YESNOCANCEL_IDCANCEL				0x00004000
            #define MB_YESNOCANCEL_MASK				0x0000F000
            // 5. 예/아니오(MB_YESNO) : IDYES(6), IDNO(7)
            #define MB_YESNO_IDYES					0x00010000
            #define MB_YESNO_IDNO					0x00020000
            #define MB_YESNO_MASK					0x000F0000
            // 6. 재시도/취소(MB_RETRYCANCEL) : IDRETRY(4), IDCANCEL(2)
            #define MB_RETRYCANCEL_IDRETRY				0x00100000
            #define MB_RETRYCANCEL_IDCANCEL				0x00200000
            #define MB_RETRYCANCEL_MASK				0x00F00000

        :return:
            실행 전의 MessageBoxMode
        """
        return self.hwp.SetMessageBoxMode(Mode=mode)

    def set_pos(self, list, para, pos):
        """
        캐럿을 문서 내 특정 위치로 옮긴다.
        지정된 위치로 캐럿을 옮겨준다.

        :param list:
            캐럿이 위치한 문서 내 list ID

        :param para:
            캐럿이 위치한 문단 ID. 음수거나, 범위를 넘어가면 문서의 시작으로 이동하며, pos는 무시한다.

        :param pos:
            캐럿이 위치한 문단 내 글자 위치. -1을 주면 해당문단의 끝으로 이동한다.
            단 para가 범위 밖일 경우 pos는 무시되고 문서의 시작으로 캐럿을 옮긴다.

        :return:
            성공하면 True, 실패하면 False
        """
        return self.hwp.SetPos(List=list, Para=para, pos=pos)

    def set_pos_by_set(self, disp_val):
        """
        캐럿을 ParameterSet으로 얻어지는 위치로 옮긴다.

        :param disp_val:
            캐럿을 옮길 위치에 대한 ParameterSet 정보

        :return:
            성공하면 True, 실패하면 False

        Examples:
            >>> start_pos = self.hwp.GetPosBySet()  # 현재 위치를 저장하고,
            >>> self.hwp.set_pos_by_set(start_pos)  # 특정 작업 후에 저장위치로 재이동
        """
        return self.hwp.SetPosBySet(dispVal=disp_val)

    def set_private_info_password(self, password):
        """
        개인정보보호를 위한 암호를 등록한다.
        개인정보 보호를 설정하기 위해서는
        우선 개인정보 보호 암호를 먼저 설정해야 한다.
        그러므로 개인정보 보호 함수를 실행하기 이전에
        반드시 이 함수를 호출해야 한다.
        (현재 작동하지 않는다.)

        :param password:
            새 암호

        :return:
            정상적으로 암호가 설정되면 true를 반환한다.
            암호설정에 실패하면 false를 반환한다. false를 반환하는 경우는 다음과 같다
            1. 암호의 길이가 너무 짧거나 너무 길 때 (영문: 5~44자, 한글: 3~22자)
            2. 암호가 이미 설정되었음. 또는 암호가 이미 설정된 문서임
        """
        return self.hwp.SetPrivateInfoPassword(Password=password)

    def set_text_file(self, data: str, format="HWPML2X", option=""):
        """
        문서를 문자열로 지정한다.

        :param data:
            문자열로 변경된 text 파일
        :param format:
            파일의 형식
            "HWP": HWP native format. BASE64 로 인코딩되어 있어야 한다. 저장된 내용을 다른 곳에서 보여줄 필요가 없다면 이 포맷을 사용하기를 권장합니다.ver:0x0505010B
            "HWPML2X": HWP 형식과 호환. 문서의 모든 정보를 유지
            "HTML": 인터넷 문서 HTML 형식. 한/글 고유의 서식은 손실된다.
            "UNICODE": 유니코드 텍스트, 서식정보가 없는 텍스트만 저장
            "TEXT": 일반 텍스트, 유니코드에만 있는 정보(한자, 고어, 특수문자 등)는 모두 손실된다.

        :param option:
            "insertfile": 현재커서 이후에 지정된 파일 삽입

        :return:
            성공이면 1을, 실패하면 0을 반환한다.
        """
        return self.hwp.SetTextFile(data=data, Format=format, option=option)

    def set_title_name(self, title):
        """
        한/글 프로그램의 타이틀을 변경한다.
        파일명과 무관하게 설정할 수 있으며,
        모든 특수문자를 허용한다.

        :param title:
            변경할 타이틀 문자열

        :return:
            성공시 True
        """
        return self.hwp.SetTitleName(Title=title)

    def set_user_info(self, user_info_id, value):
        return self.hwp.SetUserInfo(userInfoId=user_info_id, Value=value)

    def set_visible(self, visible):
        """
        현재 조작중인 한/글 인스턴스의 백그라운드 숨김여부를 변경할 수 있다.

        :param visible:
            visible=False로 설정하면 현재 조작중인 한/글 인스턴스가 백그라운드로 숨겨진다.

        :return:
        """
        self.hwp.XHwpWindows.Item(0).Visible = visible

    def side_type(self, side_type):
        return self.hwp.SideType(SideType=side_type)

    def signature(self, signature):
        return self.hwp.Signature(Signature=signature)

    def slash(self, slash):
        return self.hwp.Slash(Slash=slash)

    def solar_to_lunar(self, s_year, s_month, s_day, l_year, l_month, l_day, l_leap):
        return self.hwp.SolarToLunar(sYear=s_year, sMonth=s_month, sDay=s_day,
                                     lYear=l_year, lMonth=l_month, lDay=l_day, lLeap=l_leap)

    def solar_to_lunar_by_set(self, s_year, s_month, s_day):
        return self.hwp.SolarToLunarBySet(sYear=s_year, sMonth=s_month, sDay=s_day)

    def sort_delimiter(self, sort_delimiter):
        return self.hwp.SortDelimiter(SortDelimiter=sort_delimiter)

    def strike_out(self, strike_out_type):
        return self.hwp.StrikeOut(StrikeOutType=strike_out_type)

    def style_type(self, style_type):
        return self.hwp.StyleType(StyleType=style_type)

    def subt_pos(self, subt_pos):
        return self.hwp.SubtPos(SubtPos=subt_pos)

    def table_break(self, page_break):
        return self.hwp.TableBreak(PageBreak=page_break)

    def table_format(self, table_format):
        return self.hwp.TableFormat(TableFormat=table_format)

    def table_swap_type(self, tableswap):
        return self.hwp.TableSwapType(tableswap=tableswap)

    def table_target(self, table_target):
        return self.hwp.TableTarget(TableTarget=table_target)

    def text_align(self, text_align):
        return self.hwp.TextAlign(TextAlign=text_align)

    def text_art_align(self, text_art_align):
        return self.hwp.TextArtAlign(TextArtAlign=text_art_align)

    def text_dir(self, text_direction):
        return self.hwp.TextDir(TextDirection=text_direction)

    def text_flow_type(self, text_flow):
        return self.hwp.TextFlowType(TextFlow=text_flow)

    def text_wrap_type(self, text_wrap):
        return self.hwp.TextWrapType(TextWrap=text_wrap)

    def un_select_ctrl(self):
        return self.hwp.UnSelectCtrl()

    def v_align(self, v_align):
        return self.hwp.VAlign(VAlign=v_align)

    def vert_rel(self, vert_rel):
        return self.hwp.VertRel(VertRel=vert_rel)

    def view_flag(self, view_flag):
        return self.hwp.ViewFlag(ViewFlag=view_flag)

    def watermark_brush(self, watermark_brush):
        return self.hwp.WatermarkBrush(WatermarkBrush=watermark_brush)

    def width_rel(self, width_rel):
        return self.hwp.WidthRel(WidthRel=width_rel)
