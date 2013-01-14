
#include "PlatinumFileReader.h"
namespace platinum {

// 指定のチャンクを検索してチャンクサイズを返す
// 見つからない場合はサイズ0を返す
DWORD PlatinumFileReader::FindChunk(HANDLE hFile, int nFindFrom, const char* szChunkID)
{
	if (0 <= nFindFrom)
		::SetFilePointer(hFile, nFindFrom, NULL, FILE_BEGIN);

	DWORD dwReadBytes;
	Chunk ck;
	while (ReadFile(hFile, &ck, sizeof(ck), &dwReadBytes, NULL) &&
			dwReadBytes == sizeof(ck))
	{
		if (memcmp(&ck.dwID, szChunkID, 4) == 0)
		{
			return ck.dwSize;
		}
		::SetFilePointer(hFile, ck.dwSize, NULL, FILE_CURRENT);
		SkipNullByte(hFile, ck);
	}
	return 0;
}

PlatinumFileReader::~PlatinumFileReader()
{
	Close();
}

BOOL PlatinumFileReader::Open(const char* szFilePath)
{
	HANDLE hFile;
	hFile = CreateFile(szFilePath, GENERIC_READ, FILE_SHARE_READ, NULL,
						OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
	if (hFile == INVALID_HANDLE_VALUE)
	{
		CloseHandle(hFile);
		return FALSE;
	}

	Chunk riff;
	DWORD dwReadBytes;
	
	// RIFFの確認
	ReadFile(hFile, &riff, sizeof(Chunk), &dwReadBytes, NULL);
	if (memcmp(&riff.dwID, "RIFF", sizeof(DWORD)) != 0)
	{
		CloseHandle(hFile);
		return FALSE;
	}

	// フォームタイプの確認
	DWORD dwFccType;
	ReadFile(hFile, &dwFccType, sizeof(DWORD), &dwReadBytes, NULL);
	if (memcmp(&dwFccType, "UMF_", sizeof(DWORD)) != 0)
	{
		CloseHandle(hFile);
		return FALSE;
	}

	// RIFFチャンク直下の各チャンクを取り出す
	Chunk ckParent;
	while (ReadFile(hFile, &ckParent, sizeof(ckParent), &dwReadBytes, NULL) &&
			dwReadBytes == sizeof(ckParent))
	{
		if (memcmp(&ckParent.dwID, "UMFh", 4) == 0)
		{
			ReadFile(hFile, &_header, ckParent.dwSize, &dwReadBytes, NULL);
		}
		/*
		else if (memcmp(&ckParent.dwID, "Ver_", 4) == 0)
		{
			ReadFile(hFile, &_version, ckParent.dwSize, &dwReadBytes, NULL);
		}
		else if (memcmp(&ckParent.dwID, "Zoom", 4) == 0)
		{
			ReadFile(hFile, &_wZoomRatio, ckParent.dwSize, &dwReadBytes, NULL);
		}
		else if (memcmp(&ckParent.dwID, "EEnv", 4) == 0)
		{
			ReadFile(hFile, &_env, ckParent.dwSize, &dwReadBytes, NULL);
		}
		else if (memcmp(&ckParent.dwID, "Grid", 4) == 0)
		{
			ReadFile(hFile, &_grid, ckParent.dwSize, &dwReadBytes, NULL);
		}
		else if (memcmp(&ckParent.dwID, "Hidn", 4) == 0)
		{
			DWORD dwSize;
			ReadFile(hFile, &dwSize, sizeof(DWORD), &dwReadBytes, NULL);
			_hidden.resize(dwSize);
			ReadFile(hFile, &_hidden[0], dwSize, &dwReadBytes, NULL);
		}
		*/
		else if (memcmp(&ckParent.dwID, "ColK", 4) == 0)
		{
			ReadFile(hFile, &_colorkey, ckParent.dwSize, &dwReadBytes, NULL);
		}
		else if (memcmp(&ckParent.dwID, "InvC", 4) == 0)
		{
			ReadFile(hFile, &_inv, ckParent.dwSize, &dwReadBytes, NULL);
		}
		else if (memcmp(&ckParent.dwID, "Comt", 4) == 0)
		{
			ReadString(hFile, ckParent, _strComment);
		}
		else if (memcmp(&ckParent.dwID, "LIST", 4) == 0)
		{
			DWORD dwListTerm = SetFilePointer(hFile, 0, NULL, FILE_CURRENT) + ckParent.dwSize;

			// フォームタイプの確認
			DWORD dwListFccType;
			ReadFile(hFile, &dwListFccType, sizeof(DWORD), &dwReadBytes, NULL);
			if (memcmp(&dwListFccType, "LAY_", sizeof(DWORD)) != 0)
			{
				// 未知のサブチャンク
				SetFilePointer(hFile, ckParent.dwSize - sizeof(dwListFccType), NULL, FILE_CURRENT);				
				SkipNullByte(hFile, ckParent);
				continue;
			}

			Layer* pLayer = new Layer;			
			
			// サブチャンクを取り出す
			Chunk ckChild;
			while (ReadFile(hFile, &ckChild, sizeof(ckChild), &dwReadBytes, NULL) &&
				dwReadBytes == sizeof(ckChild))
			{
				if (memcmp(&ckChild.dwID, "LSTR", 4) == 0)
				{
					// レイヤー名
					ReadString(hFile, ckChild, pLayer->strName);
				}
				else if (memcmp(&ckChild.dwID, "PSTR", 4) == 0)
				{
					// レイヤー画像のパス
					ReadString(hFile, ckChild, pLayer->strImage);
				}
				else if (memcmp(&ckChild.dwID, "LINV", 4) == 0)
				{
					// レイヤー表示フラグ
					BYTE byVisible;
					ReadFile(hFile, &byVisible, ckChild.dwSize, &dwReadBytes, NULL);
					pLayer->bVisible = byVisible;
				}
				else if (memcmp(&ckChild.dwID, "LDAT", 4) == 0)
				{
					// マップデータ
					pLayer->arrData.resize(ckChild.dwSize);
					if (!ReadFile(hFile, &pLayer->arrData[0], ckChild.dwSize, &dwReadBytes, NULL) ||
						dwReadBytes != ckChild.dwSize)
					{
						delete pLayer;
						CloseHandle(hFile);
						return FALSE;
					}
				}
				else
				{
					// 未知のサブチャンク
					SetFilePointer(hFile, ckChild.dwSize, NULL, FILE_CURRENT);
				}
				SkipNullByte(hFile, ckChild);

				// リストチャンクの終端ならレイヤーデータをプッシュしてチャンクから抜ける
				DWORD dwCur = SetFilePointer(hFile, 0, NULL, FILE_CURRENT);
				if (dwListTerm <= dwCur)
				{
					_layers.push_back(pLayer);
					break;
				}
			}
		}
		else
		{
			// 未知のチャンク
			SetFilePointer(hFile, ckParent.dwSize, NULL, FILE_CURRENT);
		}
		SkipNullByte(hFile, ckParent);
	}

	CloseHandle(hFile);
	return TRUE;
}

// 閉じ
void PlatinumFileReader::Close()
{
	LayerArrayItor it = _layers.begin();
	while (it != _layers.end())
	{
		//(*it)->arrData;
		delete *it;
		++it;
	}
	_layers.clear();
}

// NULLバイトが存在するなら読み飛ばす
void PlatinumFileReader::SkipNullByte(HANDLE hFile, const Chunk& ck)
{
	SetFilePointer(hFile, ck.dwSize % 2, NULL, FILE_CURRENT);
}

// チャンク文字列を読む(非NULL終端)
bool PlatinumFileReader::ReadString(HANDLE hFile, const Chunk& ck, std::string& str)
{
	DWORD dwReadBytes;
	std::vector<BYTE> v(ck.dwSize);
	if (!ReadFile(hFile, &v[0], ck.dwSize, &dwReadBytes, NULL)
		|| dwReadBytes != ck.dwSize)
	{
		return false;
	}
	std::copy(v.begin(), v.end(), std::back_inserter(str));
	return true;
}


} // namespace platinum



































